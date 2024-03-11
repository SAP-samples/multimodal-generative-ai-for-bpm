# similarity functions for comparing two bpmn instances


from multimodalgenai.bpmn_schema_helper import get_flows_with_values, get_lanes
from multimodalgenai.evaluation.list_similarity import similarity_SFA
from statistics import mean

def weighted_score(array_of_scores_with_weights):
        """ Calculates a weighted score.
            Takes an array like this: [{"score": 0.3, "weight": 5},{"score": 0.8, "weight": 6}]
        """
        numerator, denominator = 0, 0
        for score_with_weight in array_of_scores_with_weights:
            score = score_with_weight["score"]
            weight = score_with_weight["weight"]
            numerator += score * weight
            denominator += weight

        if denominator == 0: return 0
        else: return numerator / denominator

def calculate_similarity_scores(bpmn_object1, bpmn_object2, method = 'dice', similarity_threshold = 0.7):
    """Calculates similarity scores for two bpmn instances using dice_SFA"""

    #### transform bpmn objects into lists #########################################################

    def get_list(bpmn_object, sublist, attribute):
        """ Returns a list of attributes within a sublist of a bpmn_object.
            For example sublist="tasks", attribute="name" returns the list of task names"""
        return list(map(lambda t: t[attribute], filter(lambda x: x.get(attribute), bpmn_object[sublist])))


    # get task names and types, the names seem more important here
    task_names1 = get_list(bpmn_object1, "tasks", "name")
    task_types1 = get_list(bpmn_object1, "tasks", "type")
    task_names2 = get_list(bpmn_object2, "tasks", "name")
    task_types2 = get_list(bpmn_object2, "tasks", "type")

    # get event names and types, the names seem more important here
    event_names1 = get_list(bpmn_object1, "events", "name")
    event_types1 = get_list(bpmn_object1, "events", "type")
    event_names2 = get_list(bpmn_object2, "events", "name")
    event_types2 = get_list(bpmn_object2, "events", "type")

    # get gateway names and types, the names are optional in the schema
    gateway_names1 = get_list(bpmn_object1, "gateways", "name")
    gateway_types1 = get_list(bpmn_object1, "gateways", "type")
    gateway_names2 = get_list(bpmn_object2, "gateways", "name")
    gateway_types2 = get_list(bpmn_object2, "gateways", "type")

    # get sequence and message flow with tripples
    seq_flow_with_values1, mes_flow_with_values1 = get_flows_with_values(bpmn_object1)
    seq_flow_with_values2, mes_flow_with_values2 = get_flows_with_values(bpmn_object2)
    seq_flows_str1 = list(map(lambda e: " ".join(e), seq_flow_with_values1))
    seq_flows_str2 = list(map(lambda e: " ".join(e), seq_flow_with_values2))
    mes_flows_str1 = list(map(lambda e: " ".join(e), mes_flow_with_values1))
    mes_flows_str2 = list(map(lambda e: " ".join(e), mes_flow_with_values2))

    # pools and lanes
    lanes1, lanes_with_refs1 = get_lanes(bpmn_object1)
    lanes2, lanes_with_refs2 = get_lanes(bpmn_object2)


    # tasks
    task_names_sim, task_names_n_union  = similarity_SFA(task_names1, task_names2, method=method,  threshold=similarity_threshold)
    task_types_sim, task_types_n_union = similarity_SFA(task_types1, task_types2, method=method, threshold=similarity_threshold)
    tasks_overall_sim = weighted_score([
        {"score": task_names_sim, "weight": task_names_n_union},
        {"score": task_types_sim, "weight": task_types_n_union}
    ])

    # events
    event_names_sim, event_names_n_union  = similarity_SFA(event_names1, event_names2, method=method, threshold=similarity_threshold)
    event_types_sim, event_types_n_union = similarity_SFA(event_types1, event_types2, method=method, threshold=similarity_threshold)
    events_overall_sim = weighted_score([
        {"score": event_names_sim, "weight": event_names_n_union},
        {"score": event_types_sim, "weight": event_types_n_union}
    ])

    # gateways
    gateway_names_sim, gateway_names_n_union  = similarity_SFA(gateway_names1, gateway_names2, method=method, threshold=similarity_threshold)
    gateway_types_sim, gateway_types_n_union = similarity_SFA(gateway_types1, gateway_types2, method=method, threshold=similarity_threshold)
    gateways_overall_sim = weighted_score([
        {"score": gateway_names_sim, "weight": gateway_names_n_union},
        {"score": gateway_types_sim, "weight": gateway_types_n_union}
    ])

    # sequence and message flows
    sequence_flows_sim, sequence_flows_n_union  = similarity_SFA(seq_flows_str1, seq_flows_str2, method=method, threshold=similarity_threshold)
    message_flows_sim, message_flows_n_union  = similarity_SFA(mes_flows_str1, mes_flows_str2, method=method, threshold=similarity_threshold)
    flows_overall_sim = weighted_score([
        {"score": sequence_flows_sim, "weight": sequence_flows_n_union},
        {"score": message_flows_sim, "weight": message_flows_n_union}
    ])

    # lanes
    lanes_without_refs_sim, lanes_without_refs_n_union  = similarity_SFA(lanes1, lanes2, method=method, threshold=similarity_threshold)
    lanes_with_refs_sim, lanes_with_refs_n_union  = similarity_SFA(lanes_with_refs1, lanes_with_refs2, method=method, threshold=similarity_threshold)
    lanes_overall_sim = weighted_score([
        {"score": lanes_without_refs_sim, "weight": lanes_without_refs_n_union},
        {"score": lanes_with_refs_sim, "weight": lanes_with_refs_n_union}
    ])


    overall = weighted_score([
        {"score": task_names_sim, "weight": task_names_n_union},
        {"score": task_types_sim, "weight": task_types_n_union},
        {"score": event_names_sim, "weight": event_names_n_union},
        {"score": event_types_sim, "weight": event_types_n_union},
        {"score": gateway_names_sim, "weight": gateway_names_n_union},
        {"score": gateway_types_sim, "weight": gateway_types_n_union},
        {"score": sequence_flows_sim, "weight": sequence_flows_n_union},
        {"score": message_flows_sim, "weight": message_flows_n_union},
        {"score": lanes_without_refs_sim, "weight": lanes_without_refs_n_union},
        {"score": lanes_with_refs_sim, "weight": lanes_with_refs_n_union},
    ])


    similarity_scores = {
        "overall": overall,
        "tasks_overall": tasks_overall_sim,
        "task_names": task_names_sim,
        "task_types": task_types_sim,
        "events_overall": events_overall_sim,
        "event_names": event_names_sim,
        "event_types": event_types_sim,
        "gateways_overall": gateways_overall_sim,
        "gateway_names": gateway_names_sim,
        "gateway_types": gateway_types_sim,
        "flows_overall": flows_overall_sim,
        "sequence_flows": sequence_flows_sim,
        "message_flows": message_flows_sim,
        "lanes_overall": lanes_overall_sim,
        "lanes_without_refs": lanes_without_refs_sim,
        "lanes_with_refs": lanes_with_refs_sim,
    }
    return similarity_scores, overall


# def calculate_average_scores(array_of_similarity_scores):
#     """Calculates average scores from an array of similarity_scores by taking the mean for each score"""
#     avg_score = {
#         "overall": mean(map(lambda score: score["overall"], array_of_similarity_scores)),
#         "tasks_overall": mean(map(lambda score: score["tasks_overall"], array_of_similarity_scores)),
#         "task_names": mean(map(lambda score: score["task_names"], array_of_similarity_scores)),
#         "task_types": mean(map(lambda score: score["task_types"], array_of_similarity_scores)),
#         "events_overall": mean(map(lambda score: score["events_overall"], array_of_similarity_scores)),
#         "event_names": mean(map(lambda score: score["event_names"], array_of_similarity_scores)),
#         "event_types": mean(map(lambda score: score["event_types"], array_of_similarity_scores)),
#         "gateways_overall": mean(map(lambda score: score["gateways_overall"], array_of_similarity_scores)),
#         "gateway_names": mean(map(lambda score: score["gateway_names"], array_of_similarity_scores)),
#         "gateway_types": mean(map(lambda score: score["gateway_types"], array_of_similarity_scores)),
#         "flows_overall": mean(map(lambda score: score["flows_overall"], array_of_similarity_scores)),
#         "sequence_flows": mean(map(lambda score: score["sequence_flows"], array_of_similarity_scores)),
#         "message_flows": mean(map(lambda score: score["message_flows"], array_of_similarity_scores)),
#         "lanes_overall": mean(map(lambda score: score["lanes_overall"], array_of_similarity_scores)),
#         "lanes_without_refs": mean(map(lambda score: score["lanes_without_refs"], array_of_similarity_scores)),
#         "lanes_with_refs": mean(map(lambda score: score["lanes_with_refs"], array_of_similarity_scores)),
#     }
#     return avg_score
