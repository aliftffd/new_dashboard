import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import { TableVirtuoso } from 'react-virtuoso';
import SensorContext from './contexts/SensorContext';

const columns = [
  {
    width: 120,
    label: 'Time',
    dataKey: 'time',
  },
  {
    width: 120,
    label: 'Speed',
    dataKey: 'speed',
    numeric: true,
  },
  {
    width: 120,
    label: 'Distance',
    dataKey: 'distance',
    numeric: true,
  },
];

const VirtuosoTableComponents = {
  TableHead: React.forwardRef((props, ref) => <div {...props} ref={ref} />),
  TableRow: ({ item: _item, ...props }) => <TableRow {...props} />,
  TableCell: ({ item: _item, ...props }) => <TableCell {...props} />,
  TableBody: React.forwardRef((props, ref) => <div {...props} ref={ref} />),
};

function fixedHeaderContent() {
  return (
    <TableRow>
      {columns.map((column, index) => (
        <TableCell
          key={column.dataKey}
          variant="head"
          align="center"
          style={{
            width: column.width,
            borderBottom: '1px solid #ddd',
            borderRight: index !== columns.length - 1 ? '1px solid #ddd' : 'none'
          }}
          sx={{
            backgroundColor: 'background.paper',
          }}
        >
          {column.label}
        </TableCell>
      ))}
    </TableRow>
  );
}

function rowContent(index, data) {
  const row = data[index];
  return (
    <TableRow>
      {columns.map((column, colIndex) => (
        <TableCell
          key={column.dataKey}
          align={column.numeric ? 'right' : 'left'}
          style={{
            borderBottom: '1px solid #ddd',
            borderRight: colIndex !== columns.length - 1 ? '1px solid #ddd' : 'none'
          }}
        >
          {row[column.dataKey]}
        </TableCell>
      ))}
    </TableRow>
  );
}

export default function HistoryPage() {
  const { sensorData } = useContext(SensorContext);

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Box sx={{ flex: 1, padding: '1rem', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
        <Paper sx={{ height: 'calc(100vh - 8rem)', width: '90%', overflow: 'hidden', marginBottom: '0.5rem', marginTop: '0.5rem' }}>
          <TableVirtuoso
            data={sensorData}
            components={VirtuosoTableComponents}
            fixedHeaderContent={fixedHeaderContent}
            itemContent={(index) => rowContent(index, sensorData)}
          />
        </Paper>
      </Box>
      <Box sx={{ display: 'flex', justifyContent: 'center', marginBottom: '2rem' }}>
        <Link to='/'>
          <button className="back-button">Back to Home</button>
        </Link>
      </Box>
    </Box>
  );
}
