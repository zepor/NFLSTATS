import React from 'react';
import CategoryButton from './CategoryButton';

const ButtonGroup = ({ categories, onCategorySelect }) => {
  return (
    <div className="row d-flex flex-row justify-content-between align-items-center">
      <div className="btn-group">
        {categories.map((category) => (
          <CategoryButton
            key={category}
            categoryName={category}
            onCategoryClick={onCategorySelect}
          />
        ))}
      </div>
    </div>
  );
};

export default ButtonGroup;
