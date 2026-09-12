class Song:
    def __init__(self, song_id, title, artist, duration):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration

    def __str__(self):
        return (f"Song ID  : {self.song_id}\n"
                f"Title    : {self.title}\n"
                f"Artist   : {self.artist}\n"
                f"Duration : {self.duration}")

    def to_row(self):
        return f"{self.song_id:<8}{self.title:<25}{self.artist:<20}{self.duration:<8}"


class Node:
    def __init__(self, song):
        self.song = song
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def insert_first(self, song):
        new_node = Node(song)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_last(self, song):
        new_node = Node(song)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def insert_at(self, position, song):
        if position < 1 or position > self._size + 1:
            raise IndexError("Invalid position.")

        if position == 1:
            self.insert_first(song)
            return

        new_node = Node(song)
        current = self.head
        count = 1
        while count < position - 1:
            current = current.next
            count += 1
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def search(self, song_id):
        current = self.head
        while current is not None:
            if current.song.song_id == song_id:
                return current.song
            current = current.next
        return None

    def delete(self, song_id):
        if self.is_empty():
            return False

        if self.head.song.song_id == song_id:
            self.head = self.head.next
            self._size -= 1
            return True

        previous = self.head
        current = self.head.next
        while current is not None:
            if current.song.song_id == song_id:
                previous.next = current.next
                self._size -= 1
                return True
            previous = current
            current = current.next

        return False

    def display(self):
        if self.is_empty():
            print("The playlist is empty.")
            return

        print(f"{'ID':<8}{'Title':<25}{'Artist':<20}{'Duration':<8}")
        print("-" * 61)
        current = self.head
        while current is not None:
            print(current.song.to_row())
            current = current.next
        print(f"\nTotal songs: {self._size}")


class MusicPlaylistManager:
    SAMPLE_SONGS = [
        ("S001", "Perfect", "Ed Sheeran", "4:23"),
        ("S002", "Shape of You", "Ed Sheeran", "3:53"),
        ("S003", "Blinding Lights", "The Weeknd", "3:20"),
        ("S004", "Levitating", "Dua Lipa", "3:23"),
        ("S005", "Bad Guy", "Billie Eilish", "3:14"),
        ("S006", "Someone Like You", "Adele", "4:45"),
    ]

    def __init__(self):
        self.playlist = LinkedList()

    def _song_id_exists(self, song_id):
        return self.playlist.search(song_id) is not None

    def _get_new_song(self):
        print("1. Choose from sample songs")
        print("2. Enter custom song details")
        choice = input("Select an option: ").strip()

        if choice == "1":
            return self._choose_sample_song()
        return self._manual_song_entry()

    def _choose_sample_song(self):
        print("\n--- Sample Songs ---")
        index = 1
        while index <= len(MusicPlaylistManager.SAMPLE_SONGS):
            song_id, title, artist, duration = MusicPlaylistManager.SAMPLE_SONGS[index - 1]
            print(f"{index}. {title} - {artist} ({duration})")
            index += 1

        selection = self._read_int(
            f"Choose a song (1-{len(MusicPlaylistManager.SAMPLE_SONGS)}): "
        )
        if selection < 1 or selection > len(MusicPlaylistManager.SAMPLE_SONGS):
            print("Invalid selection.")
            return None

        song_id, title, artist, duration = MusicPlaylistManager.SAMPLE_SONGS[selection - 1]

        if self._song_id_exists(song_id):
            print(f"Song ID '{song_id}' is already in the playlist.")
            new_id = input("Enter a different Song ID for this copy: ").strip()
            if new_id == "" or self._song_id_exists(new_id):
                print("Invalid or duplicate ID. Cancelling add.")
                return None
            song_id = new_id

        return Song(song_id, title, artist, duration)

    def _manual_song_entry(self):
        song_id = input("Enter Song ID: ").strip()
        if self._song_id_exists(song_id):
            print("A song with that ID already exists.")
            return None
        title = input("Enter Song Title: ").strip()
        artist = input("Enter Artist: ").strip()
        duration = input("Enter Duration (mm:ss): ").strip()
        return Song(song_id, title, artist, duration)

    def add_song_beginning(self):
        print("\n--- Add Song at Beginning ---")
        song = self._get_new_song()
        if song is not None:
            self.playlist.insert_first(song)
            print("Song added at the beginning.")

    def add_song_end(self):
        print("\n--- Add Song at End ---")
        song = self._get_new_song()
        if song is not None:
            self.playlist.insert_last(song)
            print("Song added at the end.")

    def insert_song_at_position(self):
        print("\n--- Insert Song at Position ---")
        max_position = self.playlist.size() + 1
        position = self._read_int(f"Enter position (1 to {max_position}): ")
        if position < 1 or position > max_position:
            print("Invalid position.")
            return
        song = self._get_new_song()
        if song is not None:
            self.playlist.insert_at(position, song)
            print(f"Song inserted at position {position}.")

    def display_playlist(self):
        print("\n--- Playlist ---")
        self.playlist.display()

    def search_song(self):
        print("\n--- Search Song ---")
        song_id = input("Enter Song ID to search: ").strip()
        song = self.playlist.search(song_id)
        if song is None:
            print("Song not found.")
        else:
            print("Song found:")
            print(song)

    def remove_song(self):
        print("\n--- Remove Song ---")
        song_id = input("Enter Song ID to remove: ").strip()
        if self.playlist.delete(song_id):
            print("Song removed successfully.")
        else:
            print("Song not found.")

    def display_playlist_size(self):
        print("\n--- Playlist Size ---")
        print(f"Total songs: {self.playlist.size()}")

    @staticmethod
    def _read_int(prompt):
        while True:
            value = input(prompt).strip()
            if value.isdigit():
                return int(value)
            print("Invalid input. Please enter a whole number.")


def print_menu():
    print("\n===== MUSIC PLAYLIST MANAGER =====")
    print("1. Add Song at Beginning")
    print("2. Add Song at End")
    print("3. Insert Song at Position")
    print("4. Display Playlist")
    print("5. Search Song")
    print("6. Remove Song")
    print("7. Display Playlist Size")
    print("8. Exit")


def main():
    manager = MusicPlaylistManager()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            manager.add_song_beginning()
        elif choice == "2":
            manager.add_song_end()
        elif choice == "3":
            manager.insert_song_at_position()
        elif choice == "4":
            manager.display_playlist()
        elif choice == "5":
            manager.search_song()
        elif choice == "6":
            manager.remove_song()
        elif choice == "7":
            manager.display_playlist_size()
        elif choice == "8":
            print("Exiting Music Playlist Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 8.")


if __name__ == "__main__":
    main()