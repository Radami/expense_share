import { render, screen, waitFor } from '@testing-library/react';
import axios from 'axios';
import React, { act } from 'react';
import Profile from './components/profile';

jest.mock('axios');

test('renders please log in without user', async () => {

    const mockResponse = { };

    axios.get.mockResolvedValue(mockResponse);

    await act(async () => {render(<Profile />);})
    

    
    const userNameElement = await waitFor(() => screen.getByText(/Please log in/i));

    expect(userNameElement).toBeInTheDocument();
});


test('renders username and email with request', async () => {

    const mockResponse = { data: { username: 'radup', email: 'radu@gmail.com' } };

    axios.get.mockResolvedValue(mockResponse);

    render(<Profile />);
    const userNameElement = await waitFor(() => screen.getByText(/radup/i));
    expect(userNameElement).toBeInTheDocument();
    const userEmailElement = await waitFor(() => screen.getByText(/radu@gmail.com/i));
    expect(userEmailElement).toBeInTheDocument();
});
