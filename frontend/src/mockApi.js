// Mock API for demonstration purposes
const mockData = {
  login: {
    success: true,
    message: 'Login successful!'
  },
  summary: {
    total_count: 15,
    avg_flowrate: 85.5,
    avg_pressure: 2.8,
    avg_temperature: 175.2,
    equipment_type_distribution: {
      'Reactor': 5,
      'Distillation Column': 4,
      'Heat Exchanger': 3,
      'Pump': 2,
      'Valve': 1
    }
  },
  history: [{
    id: 1,
    filename: 'demo_equipment_data.csv',
    upload_date: new Date().toISOString(),
    total_count: 15
  }],
  dataset: {
    data: [
      { id: 1, equipment_type: 'Reactor', flowrate: 100.5, pressure: 3.2, temperature: 180.0 },
      { id: 2, equipment_type: 'Distillation Column', flowrate: 85.3, pressure: 2.8, temperature: 170.0 },
      { id: 3, equipment_type: 'Heat Exchanger', flowrate: 75.2, pressure: 2.5, temperature: 160.0 },
      { id: 4, equipment_type: 'Pump', flowrate: 90.1, pressure: 3.5, temperature: 175.0 },
      { id: 5, equipment_type: 'Valve', flowrate: 60.8, pressure: 2.0, temperature: 150.0 }
    ]
  }
};

export const mockApi = {
  // Simulate API delay
  delay: (ms = 1000) => new Promise(resolve => setTimeout(resolve, ms)),
  
  // Mock login
  login: async (username, password) => {
    await mockApi.delay(1000);
    if (username && password) {
      return { success: true, data: mockData.login };
    }
    throw new Error('Invalid credentials');
  },
  
  // Mock summary
  getSummary: async () => {
    await mockApi.delay(800);
    return mockData.summary;
  },
  
  // Mock history
  getHistory: async () => {
    await mockApi.delay(600);
    return mockData.history;
  },
  
  // Mock dataset
  getDataset: async (id) => {
    await mockApi.delay(700);
    return mockData.dataset;
  },
  
  // Mock upload
  uploadFile: async (file) => {
    await mockApi.delay(2000);
    return {
      message: 'File uploaded successfully',
      dataset: { id: 1, filename: file.name },
      summary: mockData.summary
    };
  }
};
