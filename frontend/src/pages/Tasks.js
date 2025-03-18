import React, { useState } from 'react';
import { useQuery } from 'react-query';
import { Link } from 'react-router-dom';
import {
  Box,
  Button,
  Chip,
  CircularProgress,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Paper,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  Typography,
} from '@mui/material';

import { fetchTasks } from '../services/api';

const getStatusColor = (status) => {
  switch (status) {
    case 'completed':
      return 'success';
    case 'running':
      return 'warning';
    case 'failed':
      return 'error';
    case 'queued':
      return 'info';
    default:
      return 'default';
  }
};

const TASK_STATUS_OPTIONS = [
  { value: 'all', label: 'All Statuses' },
  { value: 'queued', label: 'Queued' },
  { value: 'running', label: 'Running' },
  { value: 'completed', label: 'Completed' },
  { value: 'failed', label: 'Failed' },
];

const AGENT_TYPE_OPTIONS = [
  { value: 'all', label: 'All Types' },
  { value: 'recruiter', label: 'Recruiter' },
  { value: 'processor', label: 'Processor' },
  { value: 'matcher', label: 'Matcher' },
  { value: 'search', label: 'Search' },
];

const Tasks = () => {
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [statusFilter, setStatusFilter] = useState('all');
  const [agentTypeFilter, setAgentTypeFilter] = useState('all');

  const { data: tasks, isLoading } = useQuery('tasks', fetchTasks);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleStatusFilterChange = (event) => {
    setStatusFilter(event.target.value);
    setPage(0);
  };

  const handleAgentTypeFilterChange = (event) => {
    setAgentTypeFilter(event.target.value);
    setPage(0);
  };

  // Filter tasks
  const filteredTasks = tasks
    ? tasks.filter((task) => {
        const statusMatch =
          statusFilter === 'all' || task.status === statusFilter;
        const typeMatch =
          agentTypeFilter === 'all' || task.agent_type === agentTypeFilter;
        return statusMatch && typeMatch;
      })
    : [];

  // Paginate tasks
  const paginatedTasks = filteredTasks.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  if (isLoading) {
    return <CircularProgress />;
  }

  return (
    <Container maxWidth="xl">
      <Typography variant="h4" gutterBottom>
        Tasks
      </Typography>

      <Stack direction="row" spacing={2} mb={3}>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel id="status-filter-label">Status</InputLabel>
          <Select
            labelId="status-filter-label"
            id="status-filter"
            value={statusFilter}
            label="Status"
            onChange={handleStatusFilterChange}
          >
            {TASK_STATUS_OPTIONS.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ minWidth: 150 }}>
          <InputLabel id="agent-type-filter-label">Agent Type</InputLabel>
          <Select
            labelId="agent-type-filter-label"
            id="agent-type-filter"
            value={agentTypeFilter}
            label="Agent Type"
            onChange={handleAgentTypeFilterChange}
          >
            {AGENT_TYPE_OPTIONS.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Stack>

      <Paper>
        <TableContainer>
          <Table sx={{ minWidth: 650 }} aria-label="tasks table">
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Agent</TableCell>
                <TableCell>Action</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Priority</TableCell>
                <TableCell>Created At</TableCell>
                <TableCell>Completed At</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {paginatedTasks.length > 0 ? (
                paginatedTasks.map((task) => (
                  <TableRow key={task.task_id} hover>
                    <TableCell>{task.task_id}</TableCell>
                    <TableCell>
                      <Link
                        to={`/agents/${task.agent_id}`}
                        style={{ textDecoration: 'none', color: 'inherit' }}
                      >
                        {task.agent_name || task.agent_id}
                      </Link>
                    </TableCell>
                    <TableCell>{task.action}</TableCell>
                    <TableCell>
                      <Chip
                        label={task.status}
                        color={getStatusColor(task.status)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{task.priority || 0}</TableCell>
                    <TableCell>
                      {task.created_at
                        ? new Date(task.created_at).toLocaleString()
                        : 'N/A'}
                    </TableCell>
                    <TableCell>
                      {task.completed_at
                        ? new Date(task.completed_at).toLocaleString()
                        : 'N/A'}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={7} align="center">
                    No tasks found.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredTasks.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
    </Container>
  );
};

export default Tasks; 