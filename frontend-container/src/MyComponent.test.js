import React from 'react';
import { render } from '@testing-library/react';
import MyComponent from './MyComponent.jsx';

test('renders Hello from MyComponent! message', () => {
  const { getByText } = render(<MyComponent />);
  const linkElement = getByText(/Hello from MyComponent!/i);
  expect(linkElement).toBeInTheDocument();
});
