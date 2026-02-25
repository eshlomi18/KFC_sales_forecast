import { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Table, TableBody, TableCell, TableContainer, 
  TableHead, TableRow, Paper, Typography, 
  ThemeProvider, createTheme, CssBaseline, Container, Box,
  FormControl, InputLabel, Select, MenuItem, Grid, TextField,
  CircularProgress, TablePagination
} from '@mui/material';

const kfcTheme = createTheme({
  palette: {
    mode: 'light',
    primary: { main: '#e5002b' },
    background: { default: '#f4f6f8' },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [forecasts, setForecasts] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const [selectedStore, setSelectedStore] = useState('');
  const [selectedDate, setSelectedDate] = useState('');

  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  useEffect(() => {
    setLoading(true);

    const params = {
      skip: page * rowsPerPage,
      limit: rowsPerPage
    };

    if (selectedStore) params.store_id = selectedStore;
    if (selectedDate) params.forecast_date = selectedDate;

    axios.get('http://localhost:8000/api/forecasts', { params })
      .then(response => {
        setForecasts(response.data.forecasts);
        // Fallback to array length in case the backend hasn't implemented total_count
        setTotalCount(response.data.total_count || response.data.forecasts.length);
      })
      .catch(error => {
        console.error("Failed to fetch forecasts:", error);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [selectedStore, selectedDate, page, rowsPerPage]);

  // Reset pagination when a filter changes
  useEffect(() => {
    setPage(0);
  }, [selectedStore, selectedDate]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <ThemeProvider theme={kfcTheme}>
      <CssBaseline /> 
      
      <Box sx={{ display: 'flex', justifyContent: 'center', width: '100vw', bgcolor: '#f4f6f8', minHeight: '100vh', pt: 5, pb: 5 }}>
        <Container maxWidth="lg" sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          
          <Box sx={{ mb: 4, width: '100%', textAlign: 'center' }}>
            <Typography variant="h4" sx={{ fontWeight: 700, color: '#e5002b', mb: 1 }}>
              KFC Sales Forecast System
            </Typography>
            <Typography variant="subtitle1" color="text.secondary">
              Displaying {totalCount} available predictions
            </Typography>
          </Box>

          <Paper elevation={2} sx={{ p: 3, mb: 4, width: '100%', borderRadius: 2 }}>
            <Grid container spacing={3} justifyContent="center">
              <Grid item xs={12} sm={5} md={4}>
                <FormControl fullWidth sx={{ minWidth: 200 }}>
                  <InputLabel>Select Store</InputLabel>
                  <Select
                    value={selectedStore}
                    label="Select Store"
                    onChange={(e) => setSelectedStore(e.target.value)}
                  >
                    <MenuItem value=""><em>All Stores</em></MenuItem>
                    <MenuItem value="1">Store 1</MenuItem>
                    <MenuItem value="2">Store 2</MenuItem>
                    <MenuItem value="3">Store 3</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={5} md={4}>
                <TextField
                  fullWidth
                  label="Forecast Date"
                  type="date"
                  value={selectedDate}
                  onChange={(e) => setSelectedDate(e.target.value)}
                  InputLabelProps={{ shrink: true }}
                  sx={{ minWidth: 200 }}
                />
              </Grid>
            </Grid>
          </Paper>

          <Paper elevation={3} sx={{ width: '100%', borderRadius: 2, overflow: 'hidden' }}>
            <TableContainer sx={{ maxHeight: '500px' }}>
              <Table stickyHeader>
                <TableHead>
                  <TableRow>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>Date</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>Hour</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>Store ID</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>Product</TableCell>
                    <TableCell sx={{ fontWeight: 'bold', backgroundColor: '#f5f5f5' }}>Predicted Sales</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {loading ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center" sx={{ py: 5 }}>
                        <CircularProgress color="primary" />
                      </TableCell>
                    </TableRow>
                  ) : forecasts.length === 0 ? (
                    <TableRow>
                      <TableCell colSpan={5} align="center" sx={{ py: 5 }}>
                        <Typography variant="body1" color="text.secondary">
                          No forecasts found for the selected criteria.
                        </Typography>
                      </TableCell>
                    </TableRow>
                  ) : (
                    forecasts.map((row, index) => (
                      <TableRow key={index} hover>
                        <TableCell>{row.forecast_date}</TableCell>
                        <TableCell>{row.hour}</TableCell>
                        <TableCell>{row.store_id}</TableCell>
                        <TableCell>{row.product_name}</TableCell>
                        <TableCell>{row.predicted_sales}</TableCell>
                      </TableRow>
                    ))
                  )}
                </TableBody>
              </Table>
            </TableContainer>
            
            <TablePagination
              rowsPerPageOptions={[10, 25, 50, 100]}
              component="div"
              count={totalCount}
              rowsPerPage={rowsPerPage}
              page={page}
              onPageChange={handleChangePage}
              onRowsPerPageChange={handleChangeRowsPerPage}
            />
          </Paper>

        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App;