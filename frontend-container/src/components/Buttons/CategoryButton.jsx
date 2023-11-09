import React from 'react';

const CategoryButton = ({ categoryName, onCategoryClick }) => {
  return (
    <button className="btn btn-dark" type="button" onClick={() => onCategoryClick(categoryName)}>
      {categoryName}
    </button>
  );
};

export default CategoryButton;
