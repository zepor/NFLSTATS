import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import axios from "axios";
const apiUrlSubmitSupport =
  process.env.NODE_ENV === "development"
    ? "http://localhost:5000/api/submit-support"
    : import.meta.env.VITE_SUPPORT_API_URL;

const SupportModal = ({ show, onHide, emailAddress }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); // To store error messages
  const [rateLimited, setRateLimited] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  console.log("API URL for submitting support:", apiUrlSubmitSupport);

  const sendEmail = async () => {
    setErrorMessage("");
    setSuccessMessage("");
    setRateLimited(false);
    if (!name || !email || !phone || !message) {
      setErrorMessage("All fields are required.");
      return;
    }
    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/;
    if (!email.match(emailRegex)) {
      setErrorMessage("Invalid email address.");
      return;
    }
    const phoneRegex = /^\d{10}$/;
    if (!phone.match(phoneRegex)) {
      setErrorMessage("Invalid phone number.");
      return;
    }
    try {
      const response = await axios.post(apiUrlSubmitSupport, {
        name,
        email,
        phone,
        message,
      });

      if (response.status === 200) {
        setSuccessMessage("Email sent successfully.");
      }
    } catch (error) {
      if (error.response && error.response.status === 429) {
        setRateLimited(true);
        setErrorMessage(
          "You have reached the rate limit. Please try again later.",
        );
      } else {
        setErrorMessage(
          "An unexpected error occurred. Please try again later.",
        );
      }
    }
  };

  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>Contact Support</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <p>Contact us at:</p>
        <p>{emailAddress}</p>
        {errorMessage && <p className="text-danger">{errorMessage}</p>}
        {successMessage && <p className="text-success">{successMessage}</p>}
        {rateLimited && (
          <p className="text-danger">
            You can only send one message per day. Please try again tomorrow.
          </p>
        )}
        <Form>
          <Form.Group controlId="name">
            <Form.Label>Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter your name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="email">
            <Form.Label>Email</Form.Label>
            <Form.Control
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="phone">
            <Form.Label>Phone</Form.Label>
            <Form.Control
              type="tel"
              placeholder="Enter your phone number"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
            />
          </Form.Group>
          <Form.Group controlId="message">
            <Form.Label>Message</Form.Label>
            <Form.Control
              as="textarea"
              rows={4}
              placeholder="Enter your message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
            />
          </Form.Group>
        </Form>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={sendEmail}>
          Send Email
        </Button>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default SupportModal;
