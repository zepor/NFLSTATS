export const SIDEBAR_POSITION = {
  LEFT: "left",
  RIGHT: "right",
};

export const SIDEBAR_BEHAVIOR = {
  STICKY: "sticky",
  FIXED: "fixed",
  COMPACT: "compact",
};

export const LAYOUT = {
  FLUID: "fluid",
  BOXED: "boxed",
};

export const THEME = {
  DEFAULT: "default",
  COLORED: "colored",
  DARK: "dark",
  LIGHT: "light",
  // NFL teams
  CARDINALS: "cardinals",
  FALCONS: "falcons",
  RAVENS: "ravens",
  BILLS: "bills",
  PANTHERS: "panthers",
  BEARS: "bears",
  BENGALS: "bengals",
  BROWNS: "browns",
  COWBOYS: "cowboys",
  BRONCOS: "broncos",
  LIONS: "lions",
  PACKERS: "packers",
  TEXANS: "texans",
  COLTS: "colts",
  JAGUARS: "jaguars",
  CHIEFS: "chiefs",
  RAIDERS: "raiders",
  CHARGERS: "chargers",
  RAMS: "rams",
  DOLPHINS: "dolphins",
  VIKINGS: "vikings",
  PATRIOTS: "patriots",
  SAINTS: "saints",
  GIANTS: "giants",
  JETS: "jets",
  EAGLES: "eagles",
  STEELERS: "steelers",
  NINERS: "49ers",
  SEAHAWKS: "seahawks",
  BUCCANEERS: "buccaneers",
  TITANS: "titans",
  COMMANDERS: "commanders",
};

export const THEME_PALETTE_LIGHT = {
  primary: "#3B82EC",
  "primary-dark": "#1659c7",
  "primary-light": "#84aef2",
  secondary: "#495057",
  success: "#4BBF73",
  info: "#1F9BCF",
  warning: "#f0ad4e",
  danger: "#d9534f",
  white: "#fff",
  "gray-100": "#f4f7f9",
  "gray-200": "#e2e8ee",
  "gray-300": "#dee6ed",
  "gray-400": "#ced4da",
  "gray-500": "#adb5bd",
  "gray-600": "#6c757d",
  "gray-700": "#495057",
  "gray-800": "#020202",
  "gray-900": "#212529",
  black: "#000",
};

export const THEME_PALETTE_DARK = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#84aef2",
  "primary-light": "#1659c7",
  white: "#293042",
  "gray-100": "#3e4555",
  "gray-200": "#545968",
  "gray-300": "#696e7b",
  "gray-400": "#7f838e",
  "gray-500": "#9498a1",
  "gray-600": "#a9acb3",
  "gray-700": "#bfc1c6",
  "gray-800": "#d4d6d9",
  "gray-900": "#eaeaec",
  black: "#fff",
};

// Defining themes for each NFL team
export const CARDINALS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#97233F",
  "primary-light": "#000000",
};

export const FALCONS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#A71930",
  "primary-light": "#000000",
};

export const RAVENS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#241773",
  "primary-light": "#9E7C0C",
};

export const BILLS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#00338D",
  "primary-light": "#C60C30",
};

export const PANTHERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#0085CA",
  "primary-light": "#101820",
};

export const BEARS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#0B162A",
  "primary-light": "#C83803",
};

export const BENGALS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#FB4F14",
  "primary-light": "#000000",
};

export const BROWNS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#311D00",
  "primary-light": "#FF3C00",
};

export const COWBOYS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#003594",
  "primary-light": "#869397",
};

export const BRONCOS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#FB4F14",
  "primary-light": "#002244",
};

export const LIONS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#0076B6",
  "primary-light": "#B0B7BC",
};

export const PACKERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#203731",
  "primary-light": "#FFB612",
};

export const TEXANS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#03202F",
  "primary-light": "#A71930",
};

export const COLTS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#002C5F",
  "primary-light": "#A2AAAD",
};

export const JAGUARS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#006778",
  "primary-light": "#9F792C",
};

export const CHIEFS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#E31837",
  "primary-light": "#FFB81C",
};

export const RAIDERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#000000",
  "primary-light": "#A5ACAF",
};

export const CHARGERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#0080C6",
  "primary-light": "#FFC20E",
};

export const RAMS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#003594",
  "primary-light": "#FFA300",
};

export const DOLPHINS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#008E97",
  "primary-light": "#FC4C02",
};

export const VIKINGS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#4F2683",
  "primary-light": "#FFC62F",
};

export const PATRIOTS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#002244",
  "primary-light": "#C60C30",
};

export const SAINTS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#D3A625",
  "primary-light": "#101820",
};

export const GIANTS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#0B2265",
  "primary-light": "#A71930",
};

export const JETS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#203731",
  "primary-light": "#FFFFFF",
};

export const EAGLES = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#014A53",
  "primary-light": "#000000",
};

export const STEELERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#FFB612",
  "primary-light": "#101820",
};

export const NINERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#AA0000",
  "primary-light": "#B3995D",
};

export const SEAHAWKS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#002244",
  "primary-light": "#69BE28",
};

export const BUCCANEERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#D50A0A",
  "primary-light": "#34302B",
};

export const TITANS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#4B92DB",
  "primary-light": "#0C2340",
};

export const COMMANDERS = {
  ...THEME_PALETTE_LIGHT,
  "primary-dark": "#773141",
  "primary-light": "#FFB612",
};
