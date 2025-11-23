/**
 * Filter controls component for rescue categories.
 */
import './FilterControls.css';

const FILTER_OPTIONS = [
  { value: 'Reset', label: 'Reset (All)' },
  { value: 'Water Rescue', label: 'Water Rescue' },
  { value: 'Mountain or Wilderness Rescue', label: 'Mountain or Wilderness Rescue' },
  { value: 'Disaster or Individual Tracking', label: 'Disaster or Individual Tracking' },
];

const FilterControls = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div className="filter-controls">
      <h2>Rescue Category Filter</h2>
      <div className="filter-buttons">
        {FILTER_OPTIONS.map((option) => (
          <button
            key={option.value}
            className={`filter-btn ${selectedCategory === option.value ? 'active' : ''}`}
            onClick={() => onCategoryChange(option.value)}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default FilterControls;

