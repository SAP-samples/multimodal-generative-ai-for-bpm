# simplified BPMN JSON schema that is the foundation for gound truth and LLM prompting.
# it captures the most used BPMN elements as lists. 
# each element has an id, which allows cross-referencing of elements across the lists.
bpmn_schema = {
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "BPMN Schema",
  "type": "object",
  "properties": {
        "tasks": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/task"
          },
        },
        "events": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/event"
          }
        },
        "gateways": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/gateway"
          }
        },
        "pools": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/pool"
          }
        },
        "sequenceFlows": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/sequenceFlow"
          }
        },
        "messageFlows": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/messageFlow"
          }
        },
  },
  "required": ["tasks", "events", "gateways", "pools", "sequenceFlows", "messageFlows"],
  "$defs": {
    "task": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": { "enum": ["Task", "Manual", "CollapsedSubprocess", "Service", "User", "Send", "Business Rule", "Receive", "Script", "CollapsedEventSubprocess"] }
      },
      "required": ["id", "name", "type"],
      "description": "A unit of work, the job to be performed",
    },
    "event": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": { "enum": ["StartNoneEvent", "EndNoneEvent", "IntermediateMessageEventCatching", "IntermediateTimerEvent", "StartMessageEvent", "IntermediateMessageEventThrowing", "EndMessageEvent", "IntermediateConditionalEvent", "IntermediateEscalationEvent", "IntermediateErrorEvent", "EndEscalationEvent", "EndCancelEvent", "IntermediateMultipleEventThrowing", "IntermediateLinkEventThrowing", "StartTimerEvent", "IntermediateCancelEvent", "IntermediateLinkEventCatching"] }
      },
      "required": ["id", "name", "type"]
    },
    "gateway": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "type": { "enum": ["Exclusive", "Parallel", "Eventbased", "Inclusive"] }
      },
      "required": ["id", "type"]
    },
    "pool": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "lanes": {
          "type": "array",
          "items": {
            "$ref": "#/$defs/lane"
          }
        }
      },
      "required": ["id", "name", "lanes"],
      "description": "Organization or role who performs the tasks",
    },
    "lane": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "name": { "type": "string" },
        "elemRefs": {
          "type": "array",
          "items": { "type": "string" }
        }
      },
    },
    "sequenceFlow": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "sourceRef": { "type": "string" },
        "targetRef": { "type": "string" },
        "condition": { "type": "string" },
      },
      "required": ["id", "sourceRef", "targetRef"],
      "description": "Defines the execution order of activities. Activities, events and gateways within a pool must be connected with sequence flow. They can not stand alone. Pictured as an solid arrow",
    },
    "messageFlow": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "sourceRef": { "type": "string" },
        "targetRef": { "type": "string" },
        "label": { "type": "string" }
      },
      "required": ["id", "sourceRef", "targetRef"],
      "description": "Messages flow between different pools. Pictured as a an dotted arrow",
    }
  }
}