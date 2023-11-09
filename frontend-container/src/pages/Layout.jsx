import React from 'react';

function Layout({children}) {
    return (
        <>
            <header>
                <h1>NFL Statistics</h1>
            </header>
            <main>
                {children}
            </main>
        </>
    );
}

export default Layout;
