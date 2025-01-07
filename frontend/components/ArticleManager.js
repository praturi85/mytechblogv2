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