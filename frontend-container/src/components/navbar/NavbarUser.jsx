import React from "react";

import { Dropdown } from "react-bootstrap";

import { PieChart, Settings, User } from "react-feather";
import { useAuth0 } from "@auth0/auth0-react"; // Import useAuth0 hook
import avatar1 from "../../assets/img/avatars/avatar.jpg";
import LogoutButton from "../LogoutButton";

const NavbarUser = () => {
  const { user, isAuthenticated } = useAuth0();
  return (
    <Dropdown className="nav-item" align="end">
      <span className="d-inline-block d-sm-none">
        <Dropdown.Toggle as="a" className="nav-link">
          <Settings size={18} className="align-middle" />
        </Dropdown.Toggle>
      </span>
      <span className="d-none d-sm-inline-block">
        <Dropdown.Toggle as="a" className="nav-link">
          {isAuthenticated ? ( // Check if user is authenticated
            <>
              {user.picture && (
                <img
                  src={user.picture}
                  className="avatar img-fluid rounded-circle me-1"
                  alt={user.name}
                />
              )}
              <span className="text-dark">{user.name}</span>
            </>
          ) : (
            "Guest" // Display "Guest" if not authenticated
          )}
        </Dropdown.Toggle>
      </span>
      <Dropdown.Menu drop="end">
        <Dropdown.Item>
          <User size={18} className="align-middle me-2" />
          Profile
        </Dropdown.Item>
        <Dropdown.Item>
          <Settings size={18} className="align-middle me-2" />
          Settings & Privacy
        </Dropdown.Item>
        <Dropdown.Item>Help</Dropdown.Item>
        <Dropdown.Item>
          <LogoutButton>Sign out</LogoutButton>
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default NavbarUser;
