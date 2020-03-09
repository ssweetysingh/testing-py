"""Testsq for Balloonicorn's Flask app."""

import unittest
import party


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        """Code to run before every test."""

        self.client = party.app.test_client()
        party.app.config['TESTING'] = True

    def test_homepage(self):
        """Can we reach the homepage?"""

        result = self.client.get("/")
        self.assertIn(b"having a party", result.data)

    def test_no_rsvp_yet(self):
        """Do users who haven't RSVPed see the correct view?"""

        result = self.client.get("/rsvp")

        # checks error thrown by app
        self.assertIn(b"Method Not Allowed", result.data)

    def test_rsvp(self):
        """Do RSVPed users see the correct view?"""

        rsvp_info = {'name': "Jane", 'email': "jane@jane.com"}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # checks flash msg loading correctly
        self.assertIn(b"Yay!", result.data)
        # checks RSVP details loading correctly
        self.assertIn(b"Party Details", result.data)
        self.assertNotIn(b"Please RSVP", result.data)

    def test_rsvp_mel(self):
        """Can we keep Mel out?"""

        rsvp_info = {'name': 'Mel Melitpolski', 'email': 'mel@ubermelon.com'}

        result = self.client.post("/rsvp", data=rsvp_info,
                                  follow_redirects=True)

        # checks correct flash msg loading
        self.assertNotIn(b"Yay", result.data)
        self.assertIn(b"Sorry, Mel. This is kind of awkward.", result.data)

        # checks correct redirect loading
        self.assertNotIn(b"Party Details", result.data)
        self.assertIn(b"Please RSVP", result.data)


if __name__ == "__main__":
    unittest.main()
