/**
 * Animal data table component.
 */
import { useState } from 'react';
import './AnimalTable.css';

const AnimalTable = ({
  animals,
  selectedAnimal,
  onAnimalSelect,
  loading,
  pagination,
  onPageChange,
}) => {
  const [sortField, setSortField] = useState(null);
  const [sortDirection, setSortDirection] = useState('asc');

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
  };

  const sortedAnimals = [...animals].sort((a, b) => {
    if (!sortField) return 0;
    const aVal = a[sortField] || '';
    const bVal = b[sortField] || '';
    const comparison = aVal.toString().localeCompare(bVal.toString());
    return sortDirection === 'asc' ? comparison : -comparison;
  });

  const visibleColumns = [
    'animal_id',
    'name',
    'animal_type',
    'breed',
    'age_upon_outcome',
    'outcome_type',
    'sex_upon_outcome',
    'datetime',
  ];

  const handleRowClick = (animal) => {
    onAnimalSelect(animal);
  };

  const totalPages = Math.ceil(pagination.total / pagination.limit);
  const currentPage = Math.floor(pagination.skip / pagination.limit) + 1;

  return (
    <div className="animal-table-container">
      <h2>Animals</h2>
      {loading ? (
        <div className="loading">Loading animals...</div>
      ) : (
        <>
          <div className="table-wrapper">
            <table className="animal-table">
              <thead>
                <tr>
                  {visibleColumns.map((col) => (
                    <th
                      key={col}
                      onClick={() => handleSort(col)}
                      className="sortable"
                    >
                      {col.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                      {sortField === col && (
                        <span className="sort-indicator">
                          {sortDirection === 'asc' ? ' ↑' : ' ↓'}
                        </span>
                      )}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {sortedAnimals.length === 0 ? (
                  <tr>
                    <td colSpan={visibleColumns.length} className="no-data">
                      No animals found
                    </td>
                  </tr>
                ) : (
                  sortedAnimals.map((animal) => (
                    <tr
                      key={animal.id || animal._id || animal.animal_id}
                      className={
                        selectedAnimal?.id === animal.id ||
                        selectedAnimal?._id === animal._id ||
                        selectedAnimal?.animal_id === animal.animal_id
                          ? 'selected'
                          : ''
                      }
                      onClick={() => handleRowClick(animal)}
                    >
                      {visibleColumns.map((col) => (
                        <td key={col}>{animal[col] || '-'}</td>
                      ))}
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
          <div className="pagination">
            <button
              onClick={() => onPageChange(Math.max(0, pagination.skip - pagination.limit))}
              disabled={pagination.skip === 0}
            >
              Previous
            </button>
            <span>
              Page {currentPage} of {totalPages || 1} ({pagination.total} total)
            </span>
            <button
              onClick={() => onPageChange(pagination.skip + pagination.limit)}
              disabled={pagination.skip + pagination.limit >= pagination.total}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default AnimalTable;

