import json

def bpmn_to_mermaid(bpmn_json):
    """
    Transforms BPMN JSON object into Mermaid.js syntax.
    :param bpmn_json: JSON object following the BPMN schema
    :return: String in Mermaid.js syntax
    """

    # Load the JSON if it's provided as a string
    if isinstance(bpmn_json, str):
        bpmn_json = json.loads(bpmn_json)

    # Initialize Mermaid.js graph definition
    mermaid = "flowchart LR"

    subgraphs = {}

    def get_lane_name(elem_id):
        for pool in bpmn_json['pools']:
            for lane in pool['lanes']:
                if elem_id in lane["elemRefs"]: return f"{pool['name']} - {lane['name']}"
        return "no_lane"
    
    def get_lane_id(elem_id):
        for pool in bpmn_json['pools']:
            for lane in pool['lanes']:
                if elem_id in lane["elemRefs"]: return lane['id']
        return "no_lane"

    # Process tasks
    for task in bpmn_json['tasks']:
        #lane_name = get_lane_name(task['id'])
        #subgraphs.setdefault(lane_name,[]).append(f"{task['id']}[\"{task['name']} ({task['type']})\"]")
        lane_id = get_lane_id(task['id'])
        subgraphs.setdefault(lane_id,[]).append(f"{task['id']}[\"{task['name']} ({task['type']})\"]")

    # Process events
    for event in bpmn_json['events']:
        #lane_name = get_lane_name(event['id'])
        #subgraphs.setdefault(lane_name,[]).append(f"{event['id']}((\"{event['name']} ({event['type']})\"))")
        lane_id = get_lane_id(event['id'])
        subgraphs.setdefault(lane_id,[]).append(f"{event['id']}((\"{event['name']} ({event['type']})\"))")


    # Process gateways
    for gateway in bpmn_json['gateways']:
        #lane_name = get_lane_name(gateway['id'])
        #subgraphs.setdefault(lane_name,[]).append(f"{gateway['id']}{{{gateway.get('name', 'x') or 'x'}}}")
        lane_id = get_lane_id(gateway['id'])
        subgraphs.setdefault(lane_id,[]).append(f"{gateway['id']}{{{gateway.get('name', 'x') or 'x'}}}")

    # # Transform subgraphs into mermaid
    # for k, v in subgraphs.items():
    #     mermaid += f"\nsubgraph {k}"
    #     mermaid += "\n" + "\n".join(v)
    #     mermaid += "\nend"

    for pool in bpmn_json['pools']:
        lanes  = pool['lanes']
        if len(lanes) == 0: 
            # handle empty pools
            mermaid += f"\nsubgraph {pool['id']}[\"{pool['name']}\"]\nend"
        else:
            for lane in lanes:
                lane_id = lane['id']
                lane_name = f"{pool['name']} - {lane['name']}"
                mermaid += f"\nsubgraph {lane_id}[\"{lane_name}\"]"
                mermaid += "\n" + "\n".join(subgraphs[lane_id])
                mermaid += "\nend"

    
    # handle elements in no lane
    elems_no_lane  = subgraphs.get("no_lane", [])
    if elems_no_lane:
        mermaid += f"\nsubgraph no lane"
        mermaid += "\n" + "\n".join(elems_no_lane)
        mermaid += "\nend"  

    # Process message and control flows
    flows = []
    for flow in bpmn_json.get('sequenceFlows', []):
        flows.append(f"{flow['sourceRef']} --> {flow['targetRef']}")

    for flow in bpmn_json.get('messageFlows', []):
        flows.append(f"{flow['sourceRef']} -.-> {flow['targetRef']}")
    
    # Join all parts into a single string
    mermaid += "\n" + ("\n".join(flows))
    return mermaid