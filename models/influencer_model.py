import sqlite3
import tensorflow as tf
import numpy as np
from datetime import datetime

# Database setup
def initialize_database():
    connection = sqlite3.connect("influencers.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS influencers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            profile_pic TEXT,
            tags TEXT,
            bio TEXT,
            contacts TEXT,
            followers INTEGER,
            instagram_link TEXT,
            tiktok_link TEXT,
            facebook_link TEXT,
            youtube_link TEXT,
            last_updated TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY,
            influencer_id INTEGER,
            post_id TEXT,
            commenters TEXT,
            FOREIGN KEY (influencer_id) REFERENCES influencers (id)
        )
    ''')
    connection.commit()
    connection.close()

# TensorFlow model setup
def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.InputLayer(input_shape=(3,)),
        tf.keras.layers.Dense(16, activation='relu'),
        tf.keras.layers.Dense(8, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Train the model
model = build_model()
data = np.array([
    [5000, 10, 0.05],  # Influencer example
    [2000, 1, 0.01]    # Non-influencer example
])
labels = np.array([1, 0])
model.fit(data, labels, epochs=10, verbose=0)

# Check if a user is an influencer
def is_influencer(followers, following_influencers, engagement_rate):
    prediction = model.predict(np.array([[followers, following_influencers, engagement_rate]]), verbose=0)
    return prediction[0][0] > 0.5

# Save or update influencer info in the database
def save_or_update_influencer(info):
    connection = sqlite3.connect("influencers.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id FROM influencers WHERE name = ?
    ''', (info['name'],))
    row = cursor.fetchone()

    if row:
        # Update existing influencer
        cursor.execute('''
            UPDATE influencers SET 
                profile_pic = ?,
                tags = ?,
                bio = ?,
                contacts = ?,
                followers = ?,
                instagram_link = ?,
                tiktok_link = ?,
                facebook_link = ?,
                youtube_link = ?,
                last_updated = ?
            WHERE id = ?
        ''', (
            info['profile_pic'],
            info['tags'],
            info['bio'],
            info['contacts'],
            info['followers'],
            info['instagram_link'],
            info['tiktok_link'],
            info['facebook_link'],
            info['youtube_link'],
            datetime.now(),
            row[0]
        ))
    else:
        # Insert new influencer
        cursor.execute('''
            INSERT INTO influencers (
                name, profile_pic, tags, bio, contacts, followers, 
                instagram_link, tiktok_link, facebook_link, youtube_link, last_updated
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            info['name'],
            info['profile_pic'],
            info['tags'],
            info['bio'],
            info['contacts'],
            info['followers'],
            info['instagram_link'],
            info['tiktok_link'],
            info['facebook_link'],
            info['youtube_link'],
            datetime.now()
        ))

    connection.commit()
    connection.close()

# Delete influencers below the threshold
def delete_non_influencers():
    connection = sqlite3.connect("influencers.db")
    cursor = connection.cursor()
    cursor.execute('''
        DELETE FROM influencers WHERE followers < 5000
    ''')
    connection.commit()
    connection.close()

# Process commenters and check their influencer status
def process_commenters(post_id, commenters):
    connection = sqlite3.connect("influencers.db")
    cursor = connection.cursor()

    for commenter in commenters:
        if is_influencer(commenter['followers'], commenter['following_influencers'], commenter['engagement_rate']):
            save_or_update_influencer(commenter)

    cursor.execute('''
        INSERT INTO posts (post_id, commenters) VALUES (?, ?)
    ''', (post_id, ','.join([c['name'] for c in commenters])))
    connection.commit()
    connection.close()

# Update influencer information
def update_influencers(influencers_data):
    for influencer in influencers_data:
        if is_influencer(influencer['followers'], 0, 0.05):
            save_or_update_influencer(influencer)

# Main monitoring loop
def monitor_social_media():
    while True:
        # Simulate social media data scraping
        influencers_data = [
            {
                'name': 'John',
                'profile_pic': 'johnpic.jpg',
                'tags': 'health, fitness',
                'bio': 'Health enthusiast.',
                'contacts': '0722768793',
                'followers': 5500,
                'instagram_link': 'https://instagram.com/john',
                'tiktok_link': '',
                'facebook_link': 'https://facebook.com/john',
                'youtube_link': ''
            },
            {
                'name': 'Alice',
                'profile_pic': 'alicepic.jpg',
                'tags': 'travel, adventure',
                'bio': 'World traveler.',
                'contacts': '0723456789',
                'followers': 4900,
                'instagram_link': 'https://instagram.com/alice',
                'tiktok_link': 'https://tiktok.com/@alice',
                'facebook_link': '',
                'youtube_link': 'https://youtube.com/alice'
            }
        ]

        update_influencers(influencers_data)
        delete_non_influencers()

        # Simulate post analysis
        process_commenters('post123', [
            {
                'name': 'Commenter1',
                'followers': 6000,
                'following_influencers': 5,
                'engagement_rate': 0.03
            },
            {
                'name': 'Commenter2',
                'followers': 3000,
                'following_influencers': 2,
                'engagement_rate': 0.01
            }
        ])

        # Pause before next iteration (e.g., 10 minutes)
        import time
        time.sleep(600)

if __name__ == "__main__":
    initialize_database()
    monitor_social_media()