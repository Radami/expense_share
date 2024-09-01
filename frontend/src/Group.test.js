import { render, screen, waitFor } from '@testing-library/react';
import React from 'react';
import Group from './components/group';

test('renders learn react link', async () => {

    render(<Group group={{"name" :'Test'}}/>);
    const userNameElement = await waitFor(() => screen.getByText(/Test/i));

    expect(userNameElement).toBeInTheDocument();
});
