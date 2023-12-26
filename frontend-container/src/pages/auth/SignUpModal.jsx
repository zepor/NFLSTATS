// SignUpModal.js
import React from "react";
import { Modal, Button } from "react-bootstrap";
import SignUp from "../../components/auth/SignUp";

function SignUpModal({ show, onHide }) {
  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Sign Up</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <SignUp />
      </Modal.Body>
    </Modal>
  );
}

export default SignUpModal;
