import { Box, Tabs, Tab } from "@mui/material";
import { DataGrid } from "@mui/x-data-grid";

//import { DataGrid } from "@mui/x-data-grid";
import { useState } from "react";
import {
  Area,
  AreaChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  BarChart,
  Legend,
  Bar,
  LineChart,
  Line,
  // PieChart,
  // Pie,
} from "recharts";

const columns = [
  { field: "id", headerName: "CVE ID", width: 90 },
  { field: "description", headerName: "Description", width: 90 },
  { field: "pub_date", headerName: "Published Date", width: 90 },
  { field: "cve_status", headerName: "Status", width: 90 },
  {
    field: "exploitability_score",
    type: "number",
    headerName: "Exploitability Score",
    width: 90,
  },
  {
    field: "impact_score",
    type: "number",
    headerName: "Impact Score",
    width: 90,
  },
  { field: "attack_vector", headerName: "Attack Vector", width: 90 },
  { field: "base_severity", headerName: "Attack Severity", width: 90 },
];

/**
 * This is the body of the application
 *
 * @param {*} props
 * @param {*} props.results
 * @returns
 */
export default function Body({ results }) {
  const [graphs] = useState(["AreaChart", "BarChart"]);
  const [selectedGraph, setSelectedGraph] = useState(0);

  const handleChange = (_, newValue) => {
    setSelectedGraph(newValue);
  };

  return (
    <Box>
      <div
        style={{
          display: "flex",
          justifyContent: "space-around",
          flexDirection: "row",
        }}
      >
        <div>
          {results ? (
            <DataGrid
              rows={results}
              columns={columns}
              initialState={{
                pagination: {
                  paginationModel: {
                    pageSize: 15,
                  },
                },
              }}
              pageSizeOptions={[15]}
              checkboxSelection
              disableRowSelectionOnClick
            />
          ) : null}
        </div>
        <div
          style={{
            display: "flex",
            justifyContent: "space-around",
            flexDirection: "column",
            height: "85vh",
          }}
        >
          <div
            style={{
              display: "flex",
              width: "100%",
              alignContent: "center",
            }}
          >
            <Tabs value={selectedGraph} onChange={handleChange}>
              {graphs.map((graphName, index) => {
                return <Tab key={graphName} label={graphName} value={index} />;
              })}
            </Tabs>
          </div>
          <Box>
            {results ? (
              <Chart name={graphs[selectedGraph]} data={results} />
            ) : null}
          </Box>
        </div>
      </div>
    </Box>
  );
}
function Chart({ name, data }) {
  const years = {};
  data.forEach((result) => {
    const { pub_date, base_severity } = result;
    const year = new Date(pub_date).getFullYear();
    if (years[year]) {
      const [prev_count, previous_high_count] = years[year];
      const newCount = prev_count + 1;
      if (base_severity === "HIGH" || base_severity === "CRITICAL") {
        years[year] = [newCount, previous_high_count + 1];
        return;
      }
      years[year] = [newCount, previous_high_count];

      return;
    }

    years[year] = [
      1,
      base_severity === "HIGH" || base_severity === "CRITICAL" ? 1 : 0,
    ];
  });

  switch (name) {
    case "AreaChart":
      return (
        <AreaChart
          width={600}
          height={400}
          data={Object.entries(years).map(([year, [count, base_severity]]) => ({
            year,
            count,
            base_severity,
          }))}
          margin={{ top: 20, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorUv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#8884d8" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="colorPv" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#82ca9d" stopOpacity={0.8} />
              <stop offset="95%" stopColor="#82ca9d" stopOpacity={0} />
            </linearGradient>
          </defs>
          <XAxis dataKey="year" />
          <YAxis />
          <CartesianGrid strokeDasharray="3 3" />
          <Tooltip />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#8884d8"
            fillOpacity={1}
            fill="url(#colorUv)"
          />
          <Area
            type="monotone"
            dataKey="base_severity"
            stroke="#82ca9d"
            fillOpacity={1}
            fill="url(#colorPv)"
          />
        </AreaChart>
      );
    case "BarChart":
      return (
        <BarChart width={600} height={400} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="pv" fill="#8884d8" />
          <Bar dataKey="uv" fill="#82ca9d" />
        </BarChart>
      );
    case "LineChart":
      return (
        <LineChart
          width={600}
          height={400}
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="pv" stroke="#8884d8" />
          <Line type="monotone" dataKey="uv" stroke="#82ca9d" />
        </LineChart>
      );

    default:
      return null;
  }
}

// const data = [
//   {
//     name: "Page A",
//     uv: 4000,
//     pv: 2400,
//     amt: 2400,
//   },
//   {
//     name: "Page B",
//     uv: 3000,
//     pv: 1398,
//     amt: 2210,
//   },
//   {
//     name: "Page C",
//     uv: 2000,
//     pv: 9800,
//     amt: 2290,
//   },
//   {
//     name: "Page D",
//     uv: 2780,
//     pv: 3908,
//     amt: 2000,
//   },
//   {
//     name: "Page E",
//     uv: 1890,
//     pv: 4800,
//     amt: 2181,
//   },
//   {
//     name: "Page F",
//     uv: 2390,
//     pv: 3800,
//     amt: 2500,
//   },
//   {
//     name: "Page G",
//     uv: 3490,
//     pv: 4300,
//     amt: 2100,
//   },
// ];

// const data01 = [
//   {
//     name: "Group A",
//     value: 400,
//   },
//   {
//     name: "Group B",
//     value: 300,
//   },
//   {
//     name: "Group C",
//     value: 300,
//   },
//   {
//     name: "Group D",
//     value: 200,
//   },
//   {
//     name: "Group E",
//     value: 278,
//   },
//   {
//     name: "Group F",
//     value: 189,
//   },
// ];
// const data02 = [
//   {
//     name: "Group A",
//     value: 2400,
//   },
//   {
//     name: "Group B",
//     value: 4567,
//   },
//   {
//     name: "Group C",
//     value: 1398,
//   },
//   {
//     name: "Group D",
//     value: 9800,
//   },
//   {
//     name: "Group E",
//     value: 3908,
//   },
//   {
//     name: "Group F",
//     value: 4800,
//   },
// ];
