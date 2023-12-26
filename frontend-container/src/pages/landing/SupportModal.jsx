import React, { useState } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import axios from "axios";
const apiUrlSubmitSupport = import.meta.env.VITE_SUPPORT_API_URL;
const SupportModal = ({ show, onHide, emailAddress }) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [message, setMessage] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); // To store error messages
  const [rateLimited, setRateLimited] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const sendEmail = async () => {
    // Validate email and phone number formats
    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$/;
    const phoneRegex = /^\d{10}$/; // Change this regex to match your phone number format

    if (!name || !email || !phone || !message) {
      setErrorMessage("All fields are required.");
    } else if (!email.match(emailRegex)) {
      setErrorMessage("Invalid email address.");
    } else if (!phone.match(phoneRegex)) {
      setErrorMessage("Invalid phone number.");
    } else {
      // Clear previous success and error messages
      setErrorMessage("");
      setSuccessMessage("");

      try {
        // Make an HTTP POST request to your Flask backend
        const response = await axios.post(
          `${apiUrlSubmitSupport}`, // Use apiUrl variable here
          {
            name,
            email,
            phone,
            message,
          },
        );

        if (response.status === 200) {
          // The email was sent successfully
          setSuccessMessage("Email sent successfully");
        } else {
          // Handle other status codes or errors from the backend
          console.error("Failed to send email");
        }
      } catch (error) {
        // Handle any network or unexpected errors
        if (error.response && error.response.status === 429) {
          // Rate limited, show a message to the user
          setRateLimited(true);
        } else {
          console.error("An error occurred:", error);
        }
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
