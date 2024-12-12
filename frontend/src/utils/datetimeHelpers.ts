export default function formatDatetime(dateTime: string){
    const date = new Date(dateTime);

    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        timeZoneName: 'short'
    };

    return date.toLocaleString('ru-RU', options);
}
