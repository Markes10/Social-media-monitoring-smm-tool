import React, { useState } from "react";
import { Box, MenuItem, Select, Button, TextField } from "@mui/material";

const Filters = ({ onFilterChange }) => {
    const [platform, setPlatform] = useState("");
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");

    const handleFilter = () => {
        onFilterChange({ platform, startDate, endDate });
    };

    return (
        <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
            <Select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                displayEmpty
            >
                <MenuItem value="">All Platforms</MenuItem>
                <MenuItem value="Twitter">Twitter</MenuItem>
                <MenuItem value="Facebook">Facebook</MenuItem>
                <MenuItem value="Instagram">Instagram</MenuItem>
            </Select>

            <TextField
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
            />
            <TextField
                type="date"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
            />

            <Button variant="contained" onClick={handleFilter}>
                Apply Filters
            </Button>
        </Box>
    );
};

export default Filters;
