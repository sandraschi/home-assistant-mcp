const isProduction = import.meta.env.PROD || (typeof window !== "undefined" && !window.location.hostname.includes("localhost"));
export const API_BASE = isProduction ? "http://127.0.0.1:10835" : "";
