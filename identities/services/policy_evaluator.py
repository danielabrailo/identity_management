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
        }