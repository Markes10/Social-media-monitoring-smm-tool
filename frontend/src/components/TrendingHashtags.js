import React, { useEffect, useState } from "react";
import { fetchTrendingHashtags } from "../api";
import { List, ListItem, ListItemText, Typography, Box } from "@mui/material";

const TrendingHashtags = () => {
    const [hashtags, setHashtags] = useState([]);

    useEffect(() => {
        fetchTrendingHashtags().then(setHashtags);
    }, []);

    return (
        <Box sx={{ mt: 3 }}>
            <Typography variant="h6">Trending Hashtags</Typography>
            <List>
                {hashtags.map((tag, index) => (
                    <ListItem key={index}>
                        <ListItemText primary={`${tag.hashtag} (${tag.count})`} />
                    </ListItem>
                ))}
            </List>
        </Box>
    );
};

export default TrendingHashtags;
