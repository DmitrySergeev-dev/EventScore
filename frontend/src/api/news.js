export async function fetchNews() {
    const apiUrl = import.meta.env.VITE_LINE_PROVIDER_API_URL;
    const url = `${apiUrl}/news/`;

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка при получении событий:', error);
        return [];
    }
}