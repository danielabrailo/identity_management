class PolicyEvaluator:

    @staticmethod
    def evaluate(profile, policy):
        return {
            "display_name": profile.display_name if policy.can_view_display_name else None,
            "email": profile.email if policy.can_view_email else None,
            "phone": profile.phone if policy.can_view_phone else None,
            "job_title": profile.job_title if policy.can_view_job_title else None,
            "linkedin": profile.linkedin if policy.can_view_linkedin else None,
            "social_media": profile.social_media if policy.can_view_social_media else None,
            "nickname": profile.nickname if policy.can_view_nickname else None,
            "organization": profile.organization if policy.can_view_organization else None,
            "pronouns": profile.pronouns if policy.can_view_pronouns else None,
            "location": profile.location if policy.can_view_location else None,
            "university": profile.university if policy.can_view_university else None,
            "website":  profile.website if policy.can_view_website  else None,
            "bio": profile.bio if policy.can_view_bio else None,
            "preferred_contact_way": profile.preferred_contact_way if policy.can_view_preferred_contact_way else None,
        }