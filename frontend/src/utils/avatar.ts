const AVATAR_CLASSES = [
    'av-color-amber', 'av-color-moss', 'av-color-sage', 'av-color-teal',
    'av-color-sky', 'av-color-slate', 'av-color-lavender', 'av-color-plum',
    'av-color-rose', 'av-color-coral',
];

function hashName(name: string): number {
    return (name.charCodeAt(0) + (name.charCodeAt(1) || 0)) % AVATAR_CLASSES.length;
}

export function getAvatarBgClass(name: string): string {
    return AVATAR_CLASSES[hashName(name)];
}

export function getAvatarColor(name: string): string {
    const cls = AVATAR_CLASSES[hashName(name)];
    return getComputedStyle(document.documentElement).getPropertyValue(`--${cls}`).trim();
}