



// Frontend: React with Modular UI Framework (Material-UI)
import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import LandingPage from "./components/LandingPage";
import ArticleManager from "./components/ArticleManager";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/landing" element={<LandingPage />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

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

// components/ArticleManager.js
import React, { useState, useEffect } from "react";
import { Box, Paper, Typography, List, ListItem, ListItemText, Avatar } from "@mui/material";
import axios from "axios";
import CommentsBox from "./CommentsBox";

const ArticleManager = () => {
  const [articles, setArticles] = useState([]);
  const [selectedArticle, setSelectedArticle] = useState(null);

  useEffect(() => {
    axios.get("http://localhost:8000/api/articles").then((response) => {
      setArticles(response.data);
    });
  }, []);

  const handleArticleClick = (article) => {
    setSelectedArticle(article);
  };

  return (
    <Box display="flex" gap={2} mt={2}>
      {/* Left Panel: Articles List */}
      <Paper elevation={3} style={{ width: "30%", padding: "10px" }}>
        <Typography variant="h6" gutterBottom>
          Articles
        </Typography>
        <List>
          {articles.map((article) => (
            <ListItem button key={article.id} onClick={() => handleArticleClick(article)}>
              <ListItemText primary={article.title} secondary={`Category: ${article.category || "Uncategorized"}`} />
            </ListItem>
          ))}
        </List>
      </Paper>

      {/* Right Panel: Article Details */}
      <Paper elevation={3} style={{ width: "70%", padding: "10px" }}>
        {selectedArticle ? (
          <Box>
            <Typography variant="h5" gutterBottom>
              {selectedArticle.title}
            </Typography>
            <Box display="flex" alignItems="center" gap={2}>
              <Avatar src={selectedArticle.authorAvatar || "default-avatar.png"} />
              <Typography>{selectedArticle.author}</Typography>
            </Box>
            <Typography color="textSecondary" gutterBottom>
              {new Date(selectedArticle.createdAt).toLocaleString()}
            </Typography>
            <Typography>{selectedArticle.content}</Typography>
            <CommentsBox articleId={selectedArticle.id} />
          </Box>
        ) : (
          <Typography>Select an article to view details.</Typography>
        )}
      </Paper>
    </Box>
  );
};

export default ArticleManager;

// components/CommentsBox.js
import React, { useState, useEffect } from "react";
import { Box, Typography, TextField, Button } from "@mui/material";
import axios from "axios";

const CommentsBox = ({ articleId }) => {
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  useEffect(() => {
    axios.get(`http://localhost:8000/api/comments?articleId=${articleId}`).then((response) => {
      setComments(response.data);
    });
  }, [articleId]);

  const handleCommentSubmit = () => {
    if (newComment.trim()) {
      axios
        .post("http://localhost:8000/api/comments", {
          articleId,
          content: newComment,
          author: "Current User",
          createdAt: new Date().toISOString(),
        })
        .then((response) => {
          setComments([...comments, response.data]);
          setNewComment("");
        });
    }
  };

  return (
    <Box mt={4}>
      <Typography variant="h6">Comments</Typography>
      {comments.map((comment) => (
        <Box key={comment.id} mt={2}>
          <Typography variant="body1" gutterBottom>
            {comment.content}
          </Typography>
          <Typography variant="body2" color="textSecondary">
            {comment.author} - {new Date(comment.createdAt).toLocaleString()}
          </Typography>
        </Box>
      ))}
      <Box mt={2} display="flex" gap={2}>
        <TextField
          fullWidth
          variant="outlined"
          label="Add a comment"
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
        />
        <Button variant="contained" color="primary" onClick={handleCommentSubmit}>
          Submit
        </Button>
      </Box>
    </Box>
  );
};

export default CommentsBox;
