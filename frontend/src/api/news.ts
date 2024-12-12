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

export async function createNews(data: Object) {
    const apiUrl = import.meta.env.VITE_LINE_PROVIDER_API_URL;
    const url = `${apiUrl}/news/`;

    try {
        fetch(url, {
            method: 'POST', // Указываем метод запроса
            headers: {
                'Content-Type': 'application/json' // Указываем тип контента
            },
            body: JSON.stringify(data) // Преобразуем объект в JSON-строку
        })

        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка при получении событий:', error);
        return [];
    }
}

export async function deleteNews(pk: string) {
    const apiUrl = import.meta.env.VITE_LINE_PROVIDER_API_URL;
    const url = `${apiUrl}/news/${pk}`;

    try {
        fetch(url, {
            method: 'DELETE', // Указываем метод запроса
        })

        if (!response.ok) {
            throw new Error(`Ошибка сети: ${response.status} ${response.statusText}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Ошибка при получении событий:', error);
        return [];
    }
}