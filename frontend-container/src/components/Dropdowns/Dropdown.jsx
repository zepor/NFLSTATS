import React from 'react';

function Dropdown({ selected, items, onSelect, label, ...rest }) {
    // Convert items into data structure that makes sense for dropdown

    const handleSelect = item => {
       onSelect(item); // This callback should handle setting the state in the parent component
    }

    return (
        <div className="col py-2 border text-bg-light p-3 rounded w-50" data-bs-theme="dark">
            <div className="input-group-text">{label}:</div>
            <button className="btn btn-outline-secondary dropdown-toggle dropdown-end w-100 position-relative" type="button" onClick={handleSelect}>
                <div className="text-center" id="selected-season">{selected || 'Select an option'}</div>
            </button>
            <div className="dropdown-menu dropdown-menu-end px-4 position-absolute" aria-labelledby="dropdownMenuButton1"
                style={{ overflowY: 'auto', height: 'auto', maxHeight: '200px' }}>
                <input id="seasonInput" className="form-control" type="text" placeholder="Filter by Year and Season" />
                <ul id="season-dropdown" className="dropdown-menu-content">
                    {items.map((item, index) => (
                        <li key={index} onClick={() => handleSelect(item)}>
                            {item.label} {/* Assuming each item has a label property */}
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
};

export default Dropdown;
