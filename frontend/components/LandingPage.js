
// components/LandingPage.js
import React from "react";
import { Container, Typography } from "@mui/material";
import ArticleManager from "./ArticleManager";

const LandingPage = () => {
  return (
    <Container>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <ArticleManager />
    </Container>
  );
};

export default LandingPage;