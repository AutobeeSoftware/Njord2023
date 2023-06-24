;; Auto-generated. Do not edit!


(when (boundp 'ball_detection_pck::ball_location)
  (if (not (find-package "BALL_DETECTION_PCK"))
    (make-package "BALL_DETECTION_PCK"))
  (shadow 'ball_location (find-package "BALL_DETECTION_PCK")))
(unless (find-package "BALL_DETECTION_PCK::BALL_LOCATION")
  (make-package "BALL_DETECTION_PCK::BALL_LOCATION"))

(in-package "ROS")
;;//! \htmlinclude ball_location.msg.html


(defclass ball_detection_pck::ball_location
  :super ros::object
  :slots (_yellow_location _black_location _red_location _green_location _middle _isyellowfound _isredfound _isgreenfound _isblackfound ))

(defmethod ball_detection_pck::ball_location
  (:init
   (&key
    ((:yellow_location __yellow_location) 0.0)
    ((:black_location __black_location) 0.0)
    ((:red_location __red_location) 0.0)
    ((:green_location __green_location) 0.0)
    ((:middle __middle) 0.0)
    ((:isyellowfound __isyellowfound) nil)
    ((:isredfound __isredfound) nil)
    ((:isgreenfound __isgreenfound) nil)
    ((:isblackfound __isblackfound) nil)
    )
   (send-super :init)
   (setq _yellow_location (float __yellow_location))
   (setq _black_location (float __black_location))
   (setq _red_location (float __red_location))
   (setq _green_location (float __green_location))
   (setq _middle (float __middle))
   (setq _isyellowfound __isyellowfound)
   (setq _isredfound __isredfound)
   (setq _isgreenfound __isgreenfound)
   (setq _isblackfound __isblackfound)
   self)
  (:yellow_location
   (&optional __yellow_location)
   (if __yellow_location (setq _yellow_location __yellow_location)) _yellow_location)
  (:black_location
   (&optional __black_location)
   (if __black_location (setq _black_location __black_location)) _black_location)
  (:red_location
   (&optional __red_location)
   (if __red_location (setq _red_location __red_location)) _red_location)
  (:green_location
   (&optional __green_location)
   (if __green_location (setq _green_location __green_location)) _green_location)
  (:middle
   (&optional __middle)
   (if __middle (setq _middle __middle)) _middle)
  (:isyellowfound
   (&optional __isyellowfound)
   (if __isyellowfound (setq _isyellowfound __isyellowfound)) _isyellowfound)
  (:isredfound
   (&optional __isredfound)
   (if __isredfound (setq _isredfound __isredfound)) _isredfound)
  (:isgreenfound
   (&optional __isgreenfound)
   (if __isgreenfound (setq _isgreenfound __isgreenfound)) _isgreenfound)
  (:isblackfound
   (&optional __isblackfound)
   (if __isblackfound (setq _isblackfound __isblackfound)) _isblackfound)
  (:serialization-length
   ()
   (+
    ;; float32 _yellow_location
    4
    ;; float32 _black_location
    4
    ;; float32 _red_location
    4
    ;; float32 _green_location
    4
    ;; float32 _middle
    4
    ;; bool _isyellowfound
    1
    ;; bool _isredfound
    1
    ;; bool _isgreenfound
    1
    ;; bool _isblackfound
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32 _yellow_location
       (sys::poke _yellow_location (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _black_location
       (sys::poke _black_location (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _red_location
       (sys::poke _red_location (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _green_location
       (sys::poke _green_location (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _middle
       (sys::poke _middle (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; bool _isyellowfound
       (if _isyellowfound (write-byte -1 s) (write-byte 0 s))
     ;; bool _isredfound
       (if _isredfound (write-byte -1 s) (write-byte 0 s))
     ;; bool _isgreenfound
       (if _isgreenfound (write-byte -1 s) (write-byte 0 s))
     ;; bool _isblackfound
       (if _isblackfound (write-byte -1 s) (write-byte 0 s))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32 _yellow_location
     (setq _yellow_location (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _black_location
     (setq _black_location (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _red_location
     (setq _red_location (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _green_location
     (setq _green_location (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _middle
     (setq _middle (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; bool _isyellowfound
     (setq _isyellowfound (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _isredfound
     (setq _isredfound (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _isgreenfound
     (setq _isgreenfound (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; bool _isblackfound
     (setq _isblackfound (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;;
   self)
  )

(setf (get ball_detection_pck::ball_location :md5sum-) "54a985c57540e58f306ef1eae8181295")
(setf (get ball_detection_pck::ball_location :datatype-) "ball_detection_pck/ball_location")
(setf (get ball_detection_pck::ball_location :definition-)
      "float32 yellow_location
float32 black_location
float32 red_location
float32 green_location
float32 middle
bool isyellowfound
bool isredfound
bool isgreenfound
bool isblackfound


")



(provide :ball_detection_pck/ball_location "54a985c57540e58f306ef1eae8181295")


