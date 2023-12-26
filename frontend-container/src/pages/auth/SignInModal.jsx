// SignInModal.js
import React from "react";
import { Modal, Button } from "react-bootstrap";
import SignIn from "../../components/auth/SignIn";

function SignInModal({ show, onHide }) {
  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Sign In</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <SignIn />
      </Modal.Body>
    </Modal>
  );
}

export default SignInModal;
