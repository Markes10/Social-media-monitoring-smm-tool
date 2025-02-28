import React, { useEffect, useState } from "react";
import { fetchPosts } from "../api";
import { DataGrid } from "@mui/x-data-grid";
import { Box, Typography, Chip } from "@mui/material";
import Filters from "./Filters";

const DataTable = () => {
    const [posts, setPosts] = useState([]);

    const loadPosts = (filters = {}) => {
        fetchPosts(filters.platform, filters.startDate, filters.endDate).then(setPosts);
    };

    useEffect(() => {
        loadPosts();
    }, []);

    const columns = [
        { field: "id", headerName: "ID", width: 80 },
        { field: "platform", headerName: "Platform", width: 130 },
        { field: "username", headerName: "User", width: 150 },
        { field: "content", headerName: "Content", width: 300 },
        { 
            field: "sentiment", 
            headerName: "Sentiment", 
            width: 150,
            renderCell: (params) => {
                let color = "default";
                if (params.value === "Positive") color = "success";
                else if (params.value === "Negative") color = "error";
                return <Chip label={params.value} color={color} />;
            }
        },
    ];

    return (
        <Box sx={{ height: 450, width: "100%" }}>
            <Typography variant="h6" sx={{ mb: 2 }}>Social Media Posts</Typography>
            <Filters onFilterChange={loadPosts} />
            <DataGrid rows={posts} columns={columns} pageSize={5} />
        </Box>
    );
};

export default DataTable;
