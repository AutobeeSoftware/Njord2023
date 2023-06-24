; Auto-generated. Do not edit!


(cl:in-package ball_detection_pck-msg)


;//! \htmlinclude ball_location.msg.html

(cl:defclass <ball_location> (roslisp-msg-protocol:ros-message)
  ((yellow_location
    :reader yellow_location
    :initarg :yellow_location
    :type cl:float
    :initform 0.0)
   (black_location
    :reader black_location
    :initarg :black_location
    :type cl:float
    :initform 0.0)
   (red_location
    :reader red_location
    :initarg :red_location
    :type cl:float
    :initform 0.0)
   (green_location
    :reader green_location
    :initarg :green_location
    :type cl:float
    :initform 0.0)
   (middle
    :reader middle
    :initarg :middle
    :type cl:float
    :initform 0.0)
   (isyellowfound
    :reader isyellowfound
    :initarg :isyellowfound
    :type cl:boolean
    :initform cl:nil)
   (isredfound
    :reader isredfound
    :initarg :isredfound
    :type cl:boolean
    :initform cl:nil)
   (isgreenfound
    :reader isgreenfound
    :initarg :isgreenfound
    :type cl:boolean
    :initform cl:nil)
   (isblackfound
    :reader isblackfound
    :initarg :isblackfound
    :type cl:boolean
    :initform cl:nil))
)

(cl:defclass ball_location (<ball_location>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <ball_location>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'ball_location)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ball_detection_pck-msg:<ball_location> is deprecated: use ball_detection_pck-msg:ball_location instead.")))

(cl:ensure-generic-function 'yellow_location-val :lambda-list '(m))
(cl:defmethod yellow_location-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:yellow_location-val is deprecated.  Use ball_detection_pck-msg:yellow_location instead.")
  (yellow_location m))

(cl:ensure-generic-function 'black_location-val :lambda-list '(m))
(cl:defmethod black_location-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:black_location-val is deprecated.  Use ball_detection_pck-msg:black_location instead.")
  (black_location m))

(cl:ensure-generic-function 'red_location-val :lambda-list '(m))
(cl:defmethod red_location-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:red_location-val is deprecated.  Use ball_detection_pck-msg:red_location instead.")
  (red_location m))

(cl:ensure-generic-function 'green_location-val :lambda-list '(m))
(cl:defmethod green_location-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:green_location-val is deprecated.  Use ball_detection_pck-msg:green_location instead.")
  (green_location m))

(cl:ensure-generic-function 'middle-val :lambda-list '(m))
(cl:defmethod middle-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:middle-val is deprecated.  Use ball_detection_pck-msg:middle instead.")
  (middle m))

(cl:ensure-generic-function 'isyellowfound-val :lambda-list '(m))
(cl:defmethod isyellowfound-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:isyellowfound-val is deprecated.  Use ball_detection_pck-msg:isyellowfound instead.")
  (isyellowfound m))

(cl:ensure-generic-function 'isredfound-val :lambda-list '(m))
(cl:defmethod isredfound-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:isredfound-val is deprecated.  Use ball_detection_pck-msg:isredfound instead.")
  (isredfound m))

(cl:ensure-generic-function 'isgreenfound-val :lambda-list '(m))
(cl:defmethod isgreenfound-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:isgreenfound-val is deprecated.  Use ball_detection_pck-msg:isgreenfound instead.")
  (isgreenfound m))

(cl:ensure-generic-function 'isblackfound-val :lambda-list '(m))
(cl:defmethod isblackfound-val ((m <ball_location>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ball_detection_pck-msg:isblackfound-val is deprecated.  Use ball_detection_pck-msg:isblackfound instead.")
  (isblackfound m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <ball_location>) ostream)
  "Serializes a message object of type '<ball_location>"
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'yellow_location))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'black_location))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'red_location))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'green_location))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'middle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'isyellowfound) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'isredfound) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'isgreenfound) 1 0)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'isblackfound) 1 0)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <ball_location>) istream)
  "Deserializes a message object of type '<ball_location>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'yellow_location) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'black_location) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'red_location) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'green_location) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'middle) (roslisp-utils:decode-single-float-bits bits)))
    (cl:setf (cl:slot-value msg 'isyellowfound) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'isredfound) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'isgreenfound) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:setf (cl:slot-value msg 'isblackfound) (cl:not (cl:zerop (cl:read-byte istream))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<ball_location>)))
  "Returns string type for a message object of type '<ball_location>"
  "ball_detection_pck/ball_location")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'ball_location)))
  "Returns string type for a message object of type 'ball_location"
  "ball_detection_pck/ball_location")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<ball_location>)))
  "Returns md5sum for a message object of type '<ball_location>"
  "54a985c57540e58f306ef1eae8181295")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'ball_location)))
  "Returns md5sum for a message object of type 'ball_location"
  "54a985c57540e58f306ef1eae8181295")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<ball_location>)))
  "Returns full string definition for message of type '<ball_location>"
  (cl:format cl:nil "float32 yellow_location~%float32 black_location~%float32 red_location~%float32 green_location~%float32 middle~%bool isyellowfound~%bool isredfound~%bool isgreenfound~%bool isblackfound~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'ball_location)))
  "Returns full string definition for message of type 'ball_location"
  (cl:format cl:nil "float32 yellow_location~%float32 black_location~%float32 red_location~%float32 green_location~%float32 middle~%bool isyellowfound~%bool isredfound~%bool isgreenfound~%bool isblackfound~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <ball_location>))
  (cl:+ 0
     4
     4
     4
     4
     4
     1
     1
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <ball_location>))
  "Converts a ROS message object to a list"
  (cl:list 'ball_location
    (cl:cons ':yellow_location (yellow_location msg))
    (cl:cons ':black_location (black_location msg))
    (cl:cons ':red_location (red_location msg))
    (cl:cons ':green_location (green_location msg))
    (cl:cons ':middle (middle msg))
    (cl:cons ':isyellowfound (isyellowfound msg))
    (cl:cons ':isredfound (isredfound msg))
    (cl:cons ':isgreenfound (isgreenfound msg))
    (cl:cons ':isblackfound (isblackfound msg))
))
