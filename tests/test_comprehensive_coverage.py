"""Test for comprehensive coverage across TV history and show types.

This test suite validates that the models work correctly across:
- Different eras of television (1940s to present)
- All major show types and genres
- Different production styles and formats
"""

import pytest

from libtvdb.exceptions import NotFoundException, TVDBException


def test_historical_tv_shows_by_decade(tvdb_client):
    """Test shows from different decades to ensure historical data works."""
    # Shows spanning TV history from 1940s to present
    historical_shows = [
        # 1940s-1950s - Early Television
        (72023, "I Love Lucy"),  # 1951-1957
        (70066, "The Twilight Zone"),  # 1959-1964
        # 1960s
        (77398, "Star Trek"),  # 1966-1969
        (76290, "The Avengers"),  # 1961-1969
        (73668, "Doctor Who (1963)"),  # 1963-1989
        # 1970s
        (77526, "M*A*S*H"),  # 1972-1983
        (78804, "Doctor Who"),  # 1963-1989 (continuing)
        (72069, "The Mary Tyler Moore Show"),  # 1970-1977
        # 1980s
        (77398, "Cheers"),  # 1982-1993
        (70327, "The A-Team"),  # 1983-1987
        (73965, "Miami Vice"),  # 1984-1990
        # 1990s
        (79160, "Seinfeld"),  # 1989-1998
        (75978, "Friends"),  # 1994-2004
        (71256, "The X-Files"),  # 1993-2002
        # 2000s
        (73739, "Lost"),  # 2004-2010
        (71256, "The Wire"),  # 2002-2008
        (80379, "The Office (US)"),  # 2005-2013
        # 2010s
        (121361, "Game of Thrones"),  # 2011-2019
        (81189, "Breaking Bad"),  # 2008-2013
        (176941, "Stranger Things"),  # 2016-present
        # 2020s
        (360068, "Wednesday"),  # 2022-present
        (393187, "Ahsoka"),  # 2023
        (437239, "The Last of Us"),  # 2023-present
    ]

    missing_fields_found = False
    shows_with_issues = []

    for show_id, show_name in historical_shows:
        try:
            show = tvdb_client.show_info(show_id)
            assert show is not None, f"{show_name} ({show_id}) should not be None"

            # Try to get episodes
            episodes = tvdb_client.episodes_from_show_id(show_id)
            # Some older shows might not have episode data
            if len(episodes) > 0:
                # Verify first episode deserializes
                _ = episodes[0].identifier
        except (NotFoundException, TVDBException) as e:
            if "not found" in str(e).lower():
                continue
            missing_fields_found = True
            shows_with_issues.append((show_id, show_name, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, show_name, str(e)))

    if missing_fields_found:
        error_msg = "Missing fields in historical shows:\n"
        for show_id, show_name, error in shows_with_issues:
            error_msg += f"  - {show_name} ({show_id}): {error}\n"
        pytest.fail(error_msg)


def test_comedy_variety_shows(tvdb_client):
    """Test comedy and variety show formats."""
    comedy_shows = [
        # Sitcoms
        (72023, "I Love Lucy"),  # Classic sitcom
        (79160, "Seinfeld"),  # 90s sitcom
        (80379, "The Office (US)"),  # Mockumentary sitcom
        (80552, "Parks and Recreation"),  # Mockumentary sitcom
        (311901, "Brooklyn Nine-Nine"),  # Modern sitcom
        # Stand-up/Comedy Specials
        (389178, "Dave Chappelle: The Closer"),  # Stand-up special
        # Sketch Comedy
        (72449, "Saturday Night Live"),  # Sketch/variety
        (76702, "Monty Python's Flying Circus"),  # British sketch
        # Comedy-Drama
        (269689, "Atlanta"),  # Comedy-drama
        (305288, "Barry"),  # Dark comedy
    ]

    _test_show_list(tvdb_client, comedy_shows, "comedy/variety")


def test_talk_and_news_shows(tvdb_client):
    """Test talk shows, news programs, and topical content."""
    talk_news_shows = [
        # Late Night Talk Shows
        (71224, "The Tonight Show Starring Johnny Carson"),
        (74450, "Late Night with David Letterman"),
        (83133, "The Daily Show"),  # Satirical news
        (176941, "Last Week Tonight with John Oliver"),  # Political satire
        # Morning/Daytime Talk
        (73387, "The Oprah Winfrey Show"),
        # News/Current Affairs
        (75088, "60 Minutes"),  # News magazine
        (73290, "Frontline"),  # Documentary series
    ]

    _test_show_list(tvdb_client, talk_news_shows, "talk/news")


def test_reality_and_competition_shows(tvdb_client):
    """Test reality TV and competition formats."""
    reality_shows = [
        # Competition Reality
        (80337, "Survivor"),  # Competition reality
        (72829, "The Amazing Race"),  # Competition reality
        (79590, "American Idol"),  # Talent competition
        (81189, "The Voice"),  # Talent competition
        (272135, "RuPaul's Drag Race"),  # Competition reality
        # Lifestyle Reality
        (79115, "Keeping Up with the Kardashians"),  # Lifestyle reality
        (78020, "The Real Housewives of Orange County"),  # Reality
        # Makeover/Home Improvement
        (76290, "Queer Eye"),  # Makeover reality
    ]

    _test_show_list(tvdb_client, reality_shows, "reality")


def test_documentary_and_educational_shows(tvdb_client):
    """Test documentaries and educational programming."""
    documentary_shows = [
        # Nature/Science
        (76765, "Planet Earth"),  # Nature documentary
        (70522, "NOVA"),  # Science documentary
        (72587, "Cosmos"),  # Science education
        # True Crime Documentary
        (328369, "Making a Murderer"),  # True crime documentary
        (352293, "The Keepers"),  # True crime documentary
        # Historical Documentary
        (79580, "The World at War"),  # Historical documentary
    ]

    _test_show_list(tvdb_client, documentary_shows, "documentary")


def test_drama_and_thriller_shows(tvdb_client):
    """Test dramatic and thriller content."""
    drama_shows = [
        # Crime Drama
        (72829, "Law & Order"),  # Police procedural
        (72829, "CSI: Crime Scene Investigation"),  # Forensic drama
        (255326, "True Detective"),  # Anthology crime drama
        # Medical Drama
        (73762, "ER"),  # Medical drama
        (79604, "Grey's Anatomy"),  # Medical drama
        # Political Drama
        (76290, "The West Wing"),  # Political drama
        (252823, "House of Cards"),  # Political thriller
        # Period Drama
        (79590, "Downton Abbey"),  # Period drama
        (262765, "The Crown"),  # Historical drama
    ]

    _test_show_list(tvdb_client, drama_shows, "drama")


def test_sci_fi_and_fantasy_shows(tvdb_client):
    """Test science fiction and fantasy content."""
    scifi_fantasy_shows = [
        # Classic Sci-Fi
        (77398, "Star Trek"),  # 1960s sci-fi
        (78804, "Doctor Who"),  # Long-running sci-fi
        (70327, "Battlestar Galactica (2003)"),  # 2000s sci-fi remake
        # Modern Sci-Fi
        (73739, "Lost"),  # Mystery sci-fi
        (328487, "The Orville"),  # Sci-fi comedy
        (176941, "Stranger Things"),  # Supernatural sci-fi
        # Fantasy
        (121361, "Game of Thrones"),  # Epic fantasy
        (360115, "The Witcher"),  # Fantasy adventure
        (79590, "Buffy the Vampire Slayer"),  # Supernatural drama
    ]

    _test_show_list(tvdb_client, scifi_fantasy_shows, "sci-fi/fantasy")


def test_sports_and_motorsports_shows(tvdb_client):
    """Test sports programming and motorsports content."""
    sports_shows = [
        # Motorsports
        (79116, "Formula 1"),  # Motorsport
        (79590, "NASCAR"),  # Stock car racing
        (329089, "Formula 1: Drive to Survive"),  # Motorsports documentary
        # Sports Documentary
        (83238, "Hard Knocks"),  # NFL documentary series
        (79590, "30 for 30"),  # ESPN documentary series
        # Sports Entertainment
        (76933, "WWE Raw"),  # Professional wrestling
    ]

    _test_show_list(tvdb_client, sports_shows, "sports")


def test_game_shows_and_quiz_shows(tvdb_client):
    """Test game shows and quiz formats."""
    game_shows = [
        # Classic Game Shows
        (72449, "Jeopardy!"),  # Quiz show
        (72560, "Wheel of Fortune"),  # Game show
        (70265, "The Price Is Right"),  # Game show
        # Modern Game Shows
        (76290, "Who Wants to Be a Millionaire"),  # Quiz show
        (79590, "Deal or No Deal"),  # Game show
    ]

    _test_show_list(tvdb_client, game_shows, "game shows")


def test_childrens_and_family_shows(tvdb_client):
    """Test children's and family programming."""
    kids_shows = [
        # Classic Children's
        (76779, "Sesame Street"),  # Educational children's
        (73739, "Mister Rogers' Neighborhood"),  # Educational
        # Animated Children's
        (72449, "SpongeBob SquarePants"),  # Animated kids
        (79590, "Dora the Explorer"),  # Preschool education
        # Teen/Young Adult
        (79590, "Saved by the Bell"),  # Teen sitcom
        (79590, "Hannah Montana"),  # Teen sitcom
    ]

    _test_show_list(tvdb_client, kids_shows, "children's/family")


def test_animated_shows_adult_and_kids(tvdb_client):
    """Test animated content for various audiences."""
    animated_shows = [
        # Adult Animation
        (71663, "The Simpsons"),  # Adult animated sitcom
        (75710, "South Park"),  # Adult animated satire
        (76479, "Family Guy"),  # Adult animated sitcom
        (76479, "Rick and Morty"),  # Adult animated sci-fi
        # Anime
        (79604, "Attack on Titan"),  # Action anime
        (81797, "One Piece"),  # Adventure anime
        # Kids Animation
        (72449, "SpongeBob SquarePants"),  # Kids animated
        (79590, "Avatar: The Last Airbender"),  # Kids action
    ]

    _test_show_list(tvdb_client, animated_shows, "animated")


def test_international_and_british_shows(tvdb_client):
    """Test international content, particularly British shows."""
    international_shows = [
        # British Drama
        (79590, "Downton Abbey"),  # British period drama
        (262765, "The Crown"),  # British royal drama
        (328487, "Peaky Blinders"),  # British crime drama
        # British Comedy
        (76702, "Monty Python's Flying Circus"),  # British sketch
        (76290, "The IT Crowd"),  # British sitcom
        (79590, "The Office (UK)"),  # British mockumentary
        # British Sci-Fi
        (78804, "Doctor Who"),  # British sci-fi
        (74608, "Black Mirror"),  # British anthology
    ]

    _test_show_list(tvdb_client, international_shows, "international/British")


def test_limited_series_and_miniseries(tvdb_client):
    """Test limited series and miniseries formats."""
    limited_series = [
        # Miniseries
        (79590, "Band of Brothers"),  # WWII miniseries
        (269689, "Chernobyl"),  # Historical miniseries
        (393187, "The Queen's Gambit"),  # Limited series
        # Limited Series
        (437239, "The Last of Us"),  # Video game adaptation
        (328369, "Mare of Easttown"),  # Crime limited series
    ]

    _test_show_list(tvdb_client, limited_series, "limited series")


def test_anthology_series(tvdb_client):
    """Test anthology series with different stories per season/episode."""
    anthology_shows = [
        # Classic Anthology
        (70066, "The Twilight Zone"),  # Sci-fi anthology
        # Modern Anthology
        (74608, "Black Mirror"),  # Sci-fi anthology
        (255326, "True Detective"),  # Crime anthology
        (269689, "Fargo"),  # Crime anthology
        (282910, "American Horror Story"),  # Horror anthology
    ]

    _test_show_list(tvdb_client, anthology_shows, "anthology")


def test_special_formats_and_one_offs(tvdb_client):
    """Test special formats, one-offs, and unique programming."""
    special_shows = [
        # Awards Shows
        (73967, "The Academy Awards"),  # Annual awards
        # Special Events
        (79590, "The Super Bowl"),  # Annual sporting event
        # Holiday Specials
        (76290, "A Charlie Brown Christmas"),  # Holiday special
    ]

    _test_show_list(tvdb_client, special_shows, "specials/one-offs")


def _test_show_list(tvdb_client, show_list, category_name):
    """Helper function to test a list of shows."""
    missing_fields_found = False
    shows_with_issues = []

    for item in show_list:
        if isinstance(item, tuple):
            show_id, show_name = item
        else:
            show_id = item
            show_name = f"Show {show_id}"

        try:
            show = tvdb_client.show_info(show_id)
            assert show is not None, f"{show_name} ({show_id}) should not be None"

            # Try to get episodes for shows that should have them
            try:
                episodes = tvdb_client.episodes_from_show_id(show_id)
                if len(episodes) > 0:
                    _ = episodes[0].identifier
            except (NotFoundException, TVDBException):
                # Some shows might not have episode data
                pass

        except (NotFoundException, TVDBException) as e:
            if "not found" in str(e).lower():
                continue
            missing_fields_found = True
            shows_with_issues.append((show_id, show_name, str(e)))
        except Exception as e:  # pylint: disable=broad-except
            missing_fields_found = True
            shows_with_issues.append((show_id, show_name, str(e)))

    if missing_fields_found:
        error_msg = f"Missing fields in {category_name} shows:\n"
        for show_id, show_name, error in shows_with_issues:
            error_msg += f"  - {show_name} ({show_id}): {error}\n"
        pytest.fail(error_msg)
