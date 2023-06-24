// Auto-generated. Do not edit!

// (in-package ball_detection_pck.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class ball_location {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.yellow_location = null;
      this.black_location = null;
      this.red_location = null;
      this.green_location = null;
      this.middle = null;
      this.isyellowfound = null;
      this.isredfound = null;
      this.isgreenfound = null;
      this.isblackfound = null;
    }
    else {
      if (initObj.hasOwnProperty('yellow_location')) {
        this.yellow_location = initObj.yellow_location
      }
      else {
        this.yellow_location = 0.0;
      }
      if (initObj.hasOwnProperty('black_location')) {
        this.black_location = initObj.black_location
      }
      else {
        this.black_location = 0.0;
      }
      if (initObj.hasOwnProperty('red_location')) {
        this.red_location = initObj.red_location
      }
      else {
        this.red_location = 0.0;
      }
      if (initObj.hasOwnProperty('green_location')) {
        this.green_location = initObj.green_location
      }
      else {
        this.green_location = 0.0;
      }
      if (initObj.hasOwnProperty('middle')) {
        this.middle = initObj.middle
      }
      else {
        this.middle = 0.0;
      }
      if (initObj.hasOwnProperty('isyellowfound')) {
        this.isyellowfound = initObj.isyellowfound
      }
      else {
        this.isyellowfound = false;
      }
      if (initObj.hasOwnProperty('isredfound')) {
        this.isredfound = initObj.isredfound
      }
      else {
        this.isredfound = false;
      }
      if (initObj.hasOwnProperty('isgreenfound')) {
        this.isgreenfound = initObj.isgreenfound
      }
      else {
        this.isgreenfound = false;
      }
      if (initObj.hasOwnProperty('isblackfound')) {
        this.isblackfound = initObj.isblackfound
      }
      else {
        this.isblackfound = false;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type ball_location
    // Serialize message field [yellow_location]
    bufferOffset = _serializer.float32(obj.yellow_location, buffer, bufferOffset);
    // Serialize message field [black_location]
    bufferOffset = _serializer.float32(obj.black_location, buffer, bufferOffset);
    // Serialize message field [red_location]
    bufferOffset = _serializer.float32(obj.red_location, buffer, bufferOffset);
    // Serialize message field [green_location]
    bufferOffset = _serializer.float32(obj.green_location, buffer, bufferOffset);
    // Serialize message field [middle]
    bufferOffset = _serializer.float32(obj.middle, buffer, bufferOffset);
    // Serialize message field [isyellowfound]
    bufferOffset = _serializer.bool(obj.isyellowfound, buffer, bufferOffset);
    // Serialize message field [isredfound]
    bufferOffset = _serializer.bool(obj.isredfound, buffer, bufferOffset);
    // Serialize message field [isgreenfound]
    bufferOffset = _serializer.bool(obj.isgreenfound, buffer, bufferOffset);
    // Serialize message field [isblackfound]
    bufferOffset = _serializer.bool(obj.isblackfound, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type ball_location
    let len;
    let data = new ball_location(null);
    // Deserialize message field [yellow_location]
    data.yellow_location = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [black_location]
    data.black_location = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [red_location]
    data.red_location = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [green_location]
    data.green_location = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [middle]
    data.middle = _deserializer.float32(buffer, bufferOffset);
    // Deserialize message field [isyellowfound]
    data.isyellowfound = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [isredfound]
    data.isredfound = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [isgreenfound]
    data.isgreenfound = _deserializer.bool(buffer, bufferOffset);
    // Deserialize message field [isblackfound]
    data.isblackfound = _deserializer.bool(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'ball_detection_pck/ball_location';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '54a985c57540e58f306ef1eae8181295';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float32 yellow_location
    float32 black_location
    float32 red_location
    float32 green_location
    float32 middle
    bool isyellowfound
    bool isredfound
    bool isgreenfound
    bool isblackfound
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new ball_location(null);
    if (msg.yellow_location !== undefined) {
      resolved.yellow_location = msg.yellow_location;
    }
    else {
      resolved.yellow_location = 0.0
    }

    if (msg.black_location !== undefined) {
      resolved.black_location = msg.black_location;
    }
    else {
      resolved.black_location = 0.0
    }

    if (msg.red_location !== undefined) {
      resolved.red_location = msg.red_location;
    }
    else {
      resolved.red_location = 0.0
    }

    if (msg.green_location !== undefined) {
      resolved.green_location = msg.green_location;
    }
    else {
      resolved.green_location = 0.0
    }

    if (msg.middle !== undefined) {
      resolved.middle = msg.middle;
    }
    else {
      resolved.middle = 0.0
    }

    if (msg.isyellowfound !== undefined) {
      resolved.isyellowfound = msg.isyellowfound;
    }
    else {
      resolved.isyellowfound = false
    }

    if (msg.isredfound !== undefined) {
      resolved.isredfound = msg.isredfound;
    }
    else {
      resolved.isredfound = false
    }

    if (msg.isgreenfound !== undefined) {
      resolved.isgreenfound = msg.isgreenfound;
    }
    else {
      resolved.isgreenfound = false
    }

    if (msg.isblackfound !== undefined) {
      resolved.isblackfound = msg.isblackfound;
    }
    else {
      resolved.isblackfound = false
    }

    return resolved;
    }
};

module.exports = ball_location;
