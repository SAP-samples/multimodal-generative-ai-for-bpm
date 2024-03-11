### some helper function to get data from the bpmn_schema or transform it into different formats

def get_element_by_id_from_sublist(bpmn_sublist, id):
    """Returns the element with the passed id. Takes a bpmn sublist like tasks, events, ect. as an argument. """
    for item in bpmn_sublist:
        if item.get('id', "") == id:
            return item
    return ""
        

def get_flows_with_values(bpmn_instance):
    """Returns sequence and message flows. Replaces the ids with the names (for tasks, events and pools) or types (for gateways) of the references"""

    def get_ref_value(ref_id):
        task_or_event_or_pool = get_element_by_id_from_sublist(bpmn_instance["tasks"] + bpmn_instance["events"] + bpmn_instance["pools"], ref_id)
        if(task_or_event_or_pool): 
            return task_or_event_or_pool.get("name", "")
        else: 
            gateway =  get_element_by_id_from_sublist(bpmn_instance["gateways"], ref_id)
            if gateway: return gateway.get("type", "")
            else: return ""

    sequence_flows_with_values = []
    for sequence_flow in bpmn_instance["sequenceFlows"]:
        sourceValue = get_ref_value(sequence_flow["sourceRef"])
        targetValue = get_ref_value(sequence_flow["targetRef"])
        sequence_flows_with_values.append([sourceValue, sequence_flow.get("condition", ""), targetValue])

    message_flows_with_values = []
    for sequence_flow in bpmn_instance["messageFlows"]:
        sourceValue = get_ref_value(sequence_flow["sourceRef"])
        targetValue = get_ref_value(sequence_flow["targetRef"])
        message_flows_with_values.append([sourceValue, sequence_flow.get("message", ""), targetValue])

    return sequence_flows_with_values, message_flows_with_values

def get_name_by_id(bpmn_instance, id):
    """Returns the name of the element with the passed id"""
    for list in bpmn_instance.values():
        for item in list:
            if item.get('id', "") == id:
                return item.get('name', "")
    return ""

def get_lanes(bpmn_instance):
    """Returns two lists: lanes_name and lanes_with_refs. 
    lanes_name is a list of names from the lanes, where the pool and lane name are concatinated.
    lanes_with_refs has the references concatinated as well. Thereby the reference ids are replaced with the names (for tasks, events and pools) 
    or types (for gateways) of the references.
    """

    # helper function
    def get_ref_value_from_task_or_event_or_gateway(bpmn_instance, ref_id):
        task_or_event = get_element_by_id_from_sublist(bpmn_instance["tasks"] + bpmn_instance["events"], ref_id)
        if(task_or_event): 
            return task_or_event.get("name", "")
        else: 
            gateway =  get_element_by_id_from_sublist(bpmn_instance["gateways"], ref_id)
            if gateway: return gateway.get("type", "")
            else: return ""

    lanes_name = []
    lanes_with_refs = []
    for pool in bpmn_instance["pools"]:
        lanes = pool["lanes"]
        if not lanes: 
            lanes_name.append(pool["name"])
        for lane in lanes:
            lane_and_pool_name = pool.get('name', "") + " - " + lane.get('name', "")
            lanes_name.append(lane_and_pool_name)
            for ref in lane.get("elemRefs", []):
                ref_value = get_ref_value_from_task_or_event_or_gateway(bpmn_instance, ref)
                lanes_with_refs.append(f"{lane_and_pool_name} - {ref_value}")

    return lanes_name, lanes_with_refs

def get_tasks_events_gateways_only(bpmn_instance):
  """Returns the task, event and gateway lists of the bpmn_instance"""
  return {
    "tasks": bpmn_instance["tasks"],
    "events": bpmn_instance["events"],
    "gateways" : bpmn_instance["gateways"]
  }

def get_tasks_events_gateways_pools_only(bpmn_instance):
  """Returns the task, event and gateway and pool lists of the bpmn_instance"""
  return {
    "tasks": bpmn_instance["tasks"],
    "events": bpmn_instance["events"],
    "gateways" : bpmn_instance["gateways"],
    "pools" : bpmn_instance["pools"]
  }

def get_seq_and_mes_flow_only(bpmn_instance):
  """Returns the seuqnec and message flow lists of the bpmn_instance"""
  return {
    "sequenceFlows": bpmn_instance["sequenceFlows"],
    "messageFlows": bpmn_instance["messageFlows"],
  }