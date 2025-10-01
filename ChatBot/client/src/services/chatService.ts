import { ChatResponse } from '../types/chat';

export async function sendMessage(message: string, apiUrl: string): Promise<string> {
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      throw new Error(`API request failed: ${response.status} ${response.statusText}`);
    }

    const data: ChatResponse = await response.json();

    if (data.error) {
      throw new Error(data.error);
    }

    return data.response || 'No response from server';
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Failed to connect to chatbot service: ${error.message}`);
    }
    throw new Error('An unexpected error occurred');
  }
}
