import React from "react";
import { Button } from "@mui/material";
import { downloadReport } from "../api";

const DownloadReport = () => {
    return (
        <Button variant="contained" color="secondary" onClick={downloadReport}>
            Download Report
        </Button>
    );
};

export default DownloadReport;
