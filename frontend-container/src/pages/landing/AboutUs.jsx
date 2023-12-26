import React from "react";
import { Button, Modal } from "react-bootstrap";

const AboutUsModal = ({ show, onHide }) => {
  return (
    <Modal show={show} onHide={onHide}>
      <Modal.Header closeButton>
        <Modal.Title>About LoveofSportsLLC</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {show && (
          <>
            <p>
              LoveofSportsLLC is a passionate sports community dedicated to
              bringing sports enthusiasts together. Our mission is to promote
              love of sports and provide a platform for fans to connect and
              share their passion.
            </p>
            <p>
              We are committed to providing high-quality content, organizing
              events, and fostering a sense of community among sports fans from
              all over the world.
            </p>
            <p>
              To support our mission and help us continue our work, please
              consider becoming a sponsor on our{" "}
              <a
                href="https://github.com/sponsors/zepor"
                target="_blank"
                rel="noopener noreferrer"
              >
                Git Sponsors page
              </a>
              .
            </p>
          </>
        )}
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default AboutUsModal;
