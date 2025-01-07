// components/Home.js
import React from "react";
import { Box, Button, Typography } from "@mui/material";
import GoogleLogin from "react-google-login";
import LinkedInLogin from "react-linkedin-login-oauth2";
import { useNavigate } from "react-router-dom";

const Home = () => {
  const navigate = useNavigate();

  const handleSuccess = (response) => {
    console.log("Login successful", response);
    navigate("/landing");
  };

  const handleFailure = (error) => {
    console.error("Login failed", error);
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      height="100vh"
      bgcolor="primary.main"
      color="white"
    >
      <Typography variant="h3" gutterBottom>
        Welcome to TechBlog
      </Typography>
      <GoogleLogin
        clientId="YOUR_GOOGLE_CLIENT_ID"
        buttonText="Sign in with Google"
        onSuccess={handleSuccess}
        onFailure={handleFailure}
        cookiePolicy="single_host_origin"
        render={(renderProps) => (
          <Button
            variant="contained"
            color="secondary"
            onClick={renderProps.onClick}
            style={{ marginBottom: "10px" }}
          >
            Sign in with Google
          </Button>
        )}
      />
      <LinkedInLogin
        clientId="YOUR_LINKEDIN_CLIENT_ID"
        redirectUri="http://localhost:3000"
        onSuccess={handleSuccess}
        onFailure={handleFailure}
        renderElement={({ onClick }) => (
          <Button variant="outlined" color="inherit" onClick={onClick}>
            Sign in with LinkedIn
          </Button>
        )}
      />
    </Box>
  );
};

export default Home;
