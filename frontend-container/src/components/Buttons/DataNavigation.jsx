import React from 'react';

function DataNavigation({onToggle}) {
    return (
        <div className="data-navigation btn-group btn-group-toggle d-flex rounded-1" data-toggle="buttons">
            {/* More similar configuration here */}
            {/* The onToggle function can be used to fetch and display data based on the selected option */}
            <label className="btn btn-dark rounded-3 focus-ring focus-ring-light w-50 d-inline-flex justify-content-center text-larger" onClick={() => onToggle('team')}>
                <input type="radio" name="dataOptions" id="teamDataBtn" autoComplete="off" defaultChecked />
                <span>Team Stats</span>
            </label>
            {/* Ensure that other radio buttons in the group are handled similarly */}
        </div>
    );
}

export default DataNavigation;
