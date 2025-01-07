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