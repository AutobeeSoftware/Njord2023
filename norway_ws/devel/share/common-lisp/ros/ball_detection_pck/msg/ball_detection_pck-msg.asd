
(cl:in-package :asdf)

(defsystem "ball_detection_pck-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "ball_location" :depends-on ("_package_ball_location"))
    (:file "_package_ball_location" :depends-on ("_package"))
  ))