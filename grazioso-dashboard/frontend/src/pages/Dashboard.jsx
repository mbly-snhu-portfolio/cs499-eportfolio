/**
 * Main dashboard page component.
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import FilterControls from '../components/FilterControls';
import AnimalTable from '../components/AnimalTable';
import AnimalMap from '../components/AnimalMap';
import BreedChart from '../components/BreedChart';
import Layout from '../components/Layout';
import { animalsAPI, analyticsAPI } from '../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const [animals, setAnimals] = useState([]);
  const [selectedAnimal, setSelectedAnimal] = useState(null);
  const [category, setCategory] = useState('Reset');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ skip: 0, limit: 100, total: 0 });
  const [breedData, setBreedData] = useState([]);

  useEffect(() => {
    loadAnimals();
    loadBreedAnalytics();
  }, [category, pagination.skip, pagination.limit]);

  const loadAnimals = async () => {
    try {
      setLoading(true);
      setError(null);
      const params = {
        skip: pagination.skip,
        limit: pagination.limit,
      };
      if (category !== 'Reset') {
        params.category = category;
      }
      const response = await animalsAPI.list(params);
      setAnimals(response.items);
      setPagination(prev => ({ ...prev, total: response.total }));
    } catch (err) {
      setError(err.message || 'Failed to load animals');
      console.error('Error loading animals:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadBreedAnalytics = async () => {
    try {
      const params = category !== 'Reset' ? { category } : {};
      const response = await analyticsAPI.getBreedAnalytics(params);
      setBreedData(response.breeds || []);
    } catch (err) {
      console.error('Error loading breed analytics:', err);
    }
  };

  const handleCategoryChange = (newCategory) => {
    setCategory(newCategory);
    setPagination(prev => ({ ...prev, skip: 0 }));
    setSelectedAnimal(null);
  };

  const handleAnimalSelect = (animal) => {
    setSelectedAnimal(animal);
  };

  const handlePageChange = (newSkip) => {
    setPagination(prev => ({ ...prev, skip: newSkip }));
  };

  return (
    <Layout user={user} onLogout={logout}>
      <div className="dashboard">
        <FilterControls
          selectedCategory={category}
          onCategoryChange={handleCategoryChange}
        />
        
        {error && <div className="error-banner">{error}</div>}
        
        <div className="dashboard-grid">
          <div className="dashboard-main">
            <AnimalTable
              animals={animals}
              selectedAnimal={selectedAnimal}
              onAnimalSelect={handleAnimalSelect}
              loading={loading}
              pagination={pagination}
              onPageChange={handlePageChange}
            />
          </div>
          
          <div className="dashboard-sidebar">
            <AnimalMap animal={selectedAnimal} />
            <BreedChart data={breedData} />
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;

