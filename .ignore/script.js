const fs = require('fs');
const path = require('path');

console.log('Script started');

(async () => {
    try {
        // Adjust the import based on how your routes are exported
        const { default: routes } = await import('./routes.mjs');
        console.log('Routes module loaded successfully');

        function createPageFile(routePath, componentPath) {
            // Adjust the directory structure for Next.js pages
            const dirPath = path.join(__dirname, 'pages', routePath);
            fs.mkdirSync(dirPath, { recursive: true });

            const filePath = path.join(dirPath, 'index.js');
            console.log(`Creating file: ${filePath}`);

            // Adjust the component import path if necessary
            const fileContent = `import Component from '../../${componentPath}';

export default function Page() {
    return <Component />;
}`;

            fs.writeFileSync(filePath, fileContent);
        }

        function processRoutes(routes, parentPath = '') {
            routes.forEach(route => {
                const routePath = path.join(parentPath, route.path);
                const componentPath = route.element.type.name;
                console.log(`Processing route: ${routePath} -> ${componentPath}`);

                createPageFile(routePath, componentPath);

                if (route.children) {
                    processRoutes(route.children, routePath);
                }
            });
        }

        processRoutes(routes);

    } catch (error) {
        console.error('Script failed:', error);
    }
})();
