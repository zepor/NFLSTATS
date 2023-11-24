import React from "react";

import { SIDEBAR_POSITION, SIDEBAR_BEHAVIOR } from "../constants";

const initialState = {
  isOpen: true,
  position: SIDEBAR_POSITION.LEFT,
  behavior: SIDEBAR_BEHAVIOR.STICKY,
};

const SidebarContext = React.createContext(initialState);

export default SidebarContext;
