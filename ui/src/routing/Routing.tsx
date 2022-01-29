import React from "react";
import { Route, Routes } from "react-router-dom";
import { AccountPage, HomePage } from "../pages";

export const Routing = () => (
  <Routes>
    <Route path="/" element={<HomePage />} />
    <Route path="/account" element={<AccountPage />} />
  </Routes>
);
