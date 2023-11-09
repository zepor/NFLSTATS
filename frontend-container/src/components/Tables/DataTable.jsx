import React from 'react';

function DataTable({headers, data}) {
    return (
        <table className="table table-striped">
            <thead className="thead-dark">
                <tr>
                    {headers.map((header, index) => (
                        <th key={index} style={{width: header.width}}>{header.name}</th>
                    ))}
                </tr>
            </thead>
            <tbody>
            {
             data.map((row, index) => (
                <tr key={index}>
                    {row.map((cell, cellIndex) => (
                        <td key={cellIndex}>{cell}</td>
                    ))}
                </tr>
             ))
            }
            </tbody>
        </table>
    );
}
export default DataTable;